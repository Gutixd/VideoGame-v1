extends Node3D

const ZONA_SEGURA_Z = -35.0
const ZONA_TREN_FANTASMA_MIN_Z = -30.0
const ZONA_TREN_FANTASMA_MAX_Z = 20.0
const CONTACTO_ENTIDAD_Z = 40.0

@onready var player: Node3D = get_node_or_null("Player")
@onready var iluminacion: Node3D = get_node_or_null("Iluminacion")

var luces_cornisa: Array = []
var luces_falladas: Dictionary = {}
var tren_fantasma_disparado := false
var contacto_entidad_disparado := false

func _ready() -> void:
	if iluminacion:
		for child in iluminacion.get_children():
			if child.name.begins_with("Luz_Cornisa"):
				luces_cornisa.append(child)
		luces_cornisa.sort_custom(func(a, b): return a.position.z < b.position.z)

func _process(_delta: float) -> void:
	if not player:
		return

	var pz = player.position.z

	_actualizar_fallo_luces(pz)

	if not tren_fantasma_disparado and pz > ZONA_TREN_FANTASMA_MIN_Z and pz < ZONA_TREN_FANTASMA_MAX_Z:
		_disparar_tren_fantasma()

	if not contacto_entidad_disparado and pz > CONTACTO_ENTIDAD_Z:
		_disparar_contacto_entidad()

func _actualizar_fallo_luces(player_z: float) -> void:
	if player_z < ZONA_SEGURA_Z:
		return

	for luz in luces_cornisa:
		if luces_falladas.has(luz):
			continue
		# Solo falla la luz mas cercana detrás del jugador (nunca por delante)
		if luz.position.z < player_z - 4.0:
			_fallar_luz(luz)
			break

func _fallar_luz(luz: OmniLight3D) -> void:
	luces_falladas[luz] = true
	var tween = create_tween()
	tween.tween_property(luz, "light_energy", 0.0, 0.4).set_trans(Tween.TRANS_EXPO)
	if has_node("Audio/ChisporroteoPlayer"):
		var audio = get_node("Audio/ChisporroteoPlayer")
		audio.global_position = luz.global_position
		audio.play()

func _disparar_tren_fantasma() -> void:
	tren_fantasma_disparado = true
	if has_node("Audio/TrenFantasmaPlayer"):
		get_node("Audio/TrenFantasmaPlayer").play()

func _disparar_contacto_entidad() -> void:
	contacto_entidad_disparado = true
	if has_node("Audio/ContactoEntidadPlayer"):
		get_node("Audio/ContactoEntidadPlayer").play()
