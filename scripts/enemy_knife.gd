extends CharacterBody3D

# Enemigo con cuchillo (ladron). Persigue al jugador y lo acuchilla de cerca.
# Toque de horror psicologico (PH): se queda QUIETO y "congelado" mientras el
# haz de la linterna del jugador lo apunta de frente; solo avanza cuando NO lo
# estas mirando/iluminando. Muere a balazos.

@export var vida := 100.0
@export var velocidad := 3.2
@export var dano := 20.0
@export var rango_ataque := 1.7
@export var rango_deteccion := 40.0
@export var cadencia_ataque := 1.1
@export var respawn_seg := 4.0

const GRAVITY := 14.0

var vida_max := 100.0
var _player: Node3D = null
var _cam: Camera3D = null
var _cooldown := 0.0
var _vivo := true

@onready var _mesh: Node3D = $Mesh
@onready var _col: CollisionShape3D = $CollisionShape3D
var _pos_inicial: Vector3
var _mesh_rot_ini: Vector3
var _mesh_pos_ini: Vector3


func _ready():
	add_to_group("enemigo")
	vida_max = vida
	_pos_inicial = global_position
	_mesh_rot_ini = _mesh.rotation_degrees
	_mesh_pos_ini = _mesh.position
	await get_tree().process_frame
	_buscar_player()


func _buscar_player():
	_player = get_tree().get_first_node_in_group("player")
	if _player:
		_cam = _player.get_node_or_null("Camera3D")


func _physics_process(delta):
	if not _vivo:
		return

	if not is_on_floor():
		velocity.y -= GRAVITY * delta
	else:
		velocity.y = 0.0

	if _player == null or not is_instance_valid(_player):
		_buscar_player()
		move_and_slide()
		return

	var hacia: Vector3 = _player.global_position - global_position
	var dist := hacia.length()
	hacia.y = 0.0

	_cooldown = max(0.0, _cooldown - delta)

	if dist <= rango_deteccion and hacia.length() > 0.05:
		# Mirar siempre al jugador
		var objetivo := global_position + hacia
		look_at(objetivo, Vector3.UP)

		if _iluminado_por_linterna():
			# PH: congelado bajo la luz -> no avanza
			velocity.x = 0.0
			velocity.z = 0.0
		elif dist > rango_ataque:
			var dir := hacia.normalized()
			velocity.x = dir.x * velocidad
			velocity.z = dir.z * velocidad
		else:
			velocity.x = 0.0
			velocity.z = 0.0
			_atacar()
	else:
		velocity.x = 0.0
		velocity.z = 0.0

	move_and_slide()


func _iluminado_por_linterna() -> bool:
	# Congela solo si el jugador tiene la linterna encendida Y el enemigo esta
	# dentro del cono frontal de la camara y relativamente cerca.
	if _cam == null:
		return false
	if "flashlight_active" in _player and not _player.flashlight_active:
		return false
	var to := global_position - _cam.global_position
	var d := to.length()
	if d > 18.0:
		return false
	var fwd := -_cam.global_transform.basis.z
	return fwd.normalized().dot(to.normalized()) > 0.9   # ~25 grados


func _atacar():
	if _cooldown <= 0.0:
		_cooldown = cadencia_ataque
		if _player and _player.has_method("recibir_dano"):
			_player.recibir_dano(dano)


func recibir_dano(d: float):
	if not _vivo:
		return
	vida -= d
	if vida <= 0.0:
		morir()


func morir():
	if not _vivo:
		return
	_vivo = false
	velocity = Vector3.ZERO
	_col.set_deferred("disabled", true)     # deja de bloquear/recibir balas

	# --- Animacion de muerte: se desploma hacia adelante y se hunde ---
	var t := create_tween()
	t.set_parallel(true)
	t.tween_property(_mesh, "rotation_degrees", _mesh_rot_ini + Vector3(-90, 0, 0), 0.5) \
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_BACK)
	t.tween_property(_mesh, "position", _mesh_pos_ini + Vector3(0, -0.25, 0.1), 0.5)

	# --- Respawn a los N segundos ---
	await get_tree().create_timer(respawn_seg).timeout
	if is_instance_valid(self):
		_respawn()


func _respawn():
	global_position = _pos_inicial
	velocity = Vector3.ZERO
	_mesh.rotation_degrees = _mesh_rot_ini
	_mesh.position = _mesh_pos_ini
	vida = vida_max
	_col.set_deferred("disabled", false)
	_vivo = true
