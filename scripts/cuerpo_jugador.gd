extends Node3D
## Cuerpo visible del jugador en primera persona ("Urban Explorer", Meshy AI).
## Fusiona 3 animaciones exportadas por separado (mismo esqueleto, 24 huesos)
## en un unico AnimationPlayer: caminar, correr, morir.
##
## Al mirar hacia abajo en primera persona se ve el propio cuerpo (piernas,
## pies); mas adelante sirve tambien como modelo de tercera persona/multijugador.

const RUTA_CAMINAR := "res://assets/models/personaje_principal_meshy/personaje_walking.glb"
const RUTA_CORRER := "res://assets/models/personaje_principal_meshy/personaje_running.glb"
const RUTA_MORIR := "res://assets/models/personaje_principal_meshy/personaje_dead.glb"

const HUESO_OJOS := "headfront"

var anim_player: AnimationPlayer
var ancla_cabeza: BoneAttachment3D
var _anim_caminar := ""
var _anim_correr := ""
var _anim_morir := ""
var _estado_actual := ""


func _ready():
	# Permite que la animacion de morir termine de reproducirse aunque el
	# menu de muerte pause el arbol justo despues de llamarla.
	process_mode = Node.PROCESS_MODE_ALWAYS
	var base: Node = load(RUTA_CAMINAR).instantiate()
	add_child(base)
	anim_player = _buscar_animation_player(base)
	if anim_player == null:
		push_error("cuerpo_jugador: no se encontro AnimationPlayer en personaje_walking.glb")
		return
	_anim_caminar = _primera_animacion(anim_player)
	_anim_correr = _fusionar_animacion(RUTA_CORRER)
	_anim_morir = _fusionar_animacion(RUTA_MORIR)

	_forzar_loop(_anim_caminar)
	_forzar_loop(_anim_correr)

	_crear_ancla_cabeza(base)

	reproducir_caminar()


func _buscar_skeleton(nodo: Node) -> Skeleton3D:
	if nodo is Skeleton3D:
		return nodo
	for hijo in nodo.get_children():
		var r := _buscar_skeleton(hijo)
		if r:
			return r
	return null


func _crear_ancla_cabeza(base: Node):
	var skel := _buscar_skeleton(base)
	if skel == null:
		push_warning("cuerpo_jugador: no se encontro Skeleton3D, la camara no seguira la animacion")
		return
	var idx := skel.find_bone(HUESO_OJOS)
	if idx == -1:
		push_warning("cuerpo_jugador: no se encontro el hueso '%s'" % HUESO_OJOS)
		return
	ancla_cabeza = BoneAttachment3D.new()
	ancla_cabeza.name = "AnclaCabeza"
	ancla_cabeza.bone_name = HUESO_OJOS
	skel.add_child(ancla_cabeza)


func _forzar_loop(nombre_completo: String):
	if anim_player == null or nombre_completo == "":
		return
	var anim := anim_player.get_animation(nombre_completo)
	if anim:
		anim.loop_mode = Animation.LOOP_LINEAR


func _buscar_animation_player(nodo: Node) -> AnimationPlayer:
	if nodo is AnimationPlayer:
		return nodo
	for hijo in nodo.get_children():
		var r := _buscar_animation_player(hijo)
		if r:
			return r
	return null


func _primera_animacion(ap: AnimationPlayer) -> String:
	for lib_name in ap.get_animation_library_list():
		var lib := ap.get_animation_library(lib_name)
		for anim_name in lib.get_animation_list():
			return (lib_name + "/" + anim_name) if lib_name != "" else anim_name
	return ""


func _fusionar_animacion(ruta_glb: String) -> String:
	var extra: Node = load(ruta_glb).instantiate()
	var ap_extra := _buscar_animation_player(extra)
	var resultado := ""
	if ap_extra:
		var nuevo_lib_name := "extra_%d" % anim_player.get_animation_library_list().size()
		for lib_name in ap_extra.get_animation_library_list():
			var lib := ap_extra.get_animation_library(lib_name)
			anim_player.add_animation_library(nuevo_lib_name, lib)
			for anim_name in lib.get_animation_list():
				resultado = nuevo_lib_name + "/" + anim_name
	extra.queue_free()
	return resultado


func reproducir_caminar():
	_reproducir(_anim_caminar)


func reproducir_correr():
	_reproducir(_anim_correr)


func reproducir_morir():
	_reproducir(_anim_morir)


func detener():
	if _estado_actual == "quieto":
		return
	_estado_actual = "quieto"
	if anim_player:
		anim_player.stop(true)  # congela la pose actual (no vuelve al bind pose)


func _reproducir(nombre: String):
	if anim_player == null or nombre == "" or _estado_actual == nombre:
		return
	_estado_actual = nombre
	anim_player.play(nombre)
