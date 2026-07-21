extends CharacterBody3D

const SPEED = 10.5
const SPRINT_SPEED = 60.0
const JUMP_VELOCITY = 20.8
const GRAVITY = 9.8
const MOUSE_SENSITIVITY = 0.003
const BOB_FREQ = 2.0
const BOB_AMP = 0.08
const FLASHLIGHT_BATTERY_MAX = 180.0

# Combate
const MAX_VIDA = 100.0
const MAX_BALAS = 100
const DANO_DISPARO = 30.0
const ALCANCE_DISPARO = 120.0
const CADENCIA_DISPARO = 0.16

@onready var camera = $Camera3D
@onready var flashlight = $Camera3D/SpotLight3D
@onready var flashlight_timer = $FlashlightTimer

var bob_time = 0.0
var camera_base_pos: Vector3
var flashlight_battery = FLASHLIGHT_BATTERY_MAX
var flashlight_active = true

# Combate
var vida = MAX_VIDA
var balas = MAX_BALAS
var _cd_disparo = 0.0
var muzzle: Node3D = null

func _ready():
	# Rampas de las escaleras del metro: snap alto para que el jugador no
	# se despegue del piso en las uniones convexas (rampa->descanso) al
	# subir/bajar, y angulo maximo generoso para pisar rampas inclinadas.
	floor_snap_length = 1.0
	floor_max_angle = deg_to_rad(55)
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	camera_base_pos = camera.position
	flashlight.visible = true
	flashlight_timer.wait_time = 1.0
	flashlight_timer.timeout.connect(_on_flashlight_tick)
	flashlight_timer.start()

func _physics_process(delta):
	_handle_movement(delta)
	_handle_camera_look(delta)
	_handle_camera_bob(delta)
	_handle_flashlight_toggle()
	_handle_interaction()
	_handle_shoot(delta)

	move_and_slide()

func _handle_shoot(delta):
	if Input.is_action_just_pressed("reload"):
		recargar_full()
	_cd_disparo = max(0.0, _cd_disparo - delta)
	if Input.is_action_pressed("shoot") and _cd_disparo <= 0.0 and balas > 0 and vida > 0.0:
		_cd_disparo = CADENCIA_DISPARO
		balas -= 1
		var origen = camera.global_position
		var dir = -camera.global_transform.basis.z
		var query = PhysicsRayQueryParameters3D.create(origen, origen + dir * ALCANCE_DISPARO)
		query.exclude = [self]
		var hit = get_world_3d().direct_space_state.intersect_ray(query)
		var destino = origen + dir * ALCANCE_DISPARO
		if hit:
			destino = hit.position
			if hit.collider and hit.collider.has_method("recibir_dano"):
				hit.collider.recibir_dano(DANO_DISPARO)
		# trazadora de bala visible (desde la boca del arma hasta el impacto)
		var boca = origen + camera.global_transform.basis.x * 0.18 \
			- camera.global_transform.basis.y * 0.12 + dir * 0.4
		_mostrar_trazo(boca, destino)

func _mostrar_trazo(desde: Vector3, hasta: Vector3):
	var d = hasta - desde
	var largo = d.length()
	if largo < 0.05:
		return
	var trazo = MeshInstance3D.new()
	var m = CylinderMesh.new()
	m.top_radius = 0.02
	m.bottom_radius = 0.02
	m.height = largo
	m.radial_segments = 6
	trazo.mesh = m
	var mat = StandardMaterial3D.new()
	mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	mat.albedo_color = Color(1.0, 0.85, 0.4)
	mat.emission_enabled = true
	mat.emission = Color(1.0, 0.8, 0.3)
	mat.emission_energy_multiplier = 4.0
	m.material = mat
	get_tree().current_scene.add_child(trazo)
	trazo.look_at_from_position((desde + hasta) * 0.5, hasta, Vector3.UP)
	trazo.rotate_object_local(Vector3(1, 0, 0), -PI / 2.0)
	var t = create_tween()
	t.tween_interval(0.05)
	t.tween_callback(trazo.queue_free)

func recibir_dano(cantidad: float):
	if vida <= 0.0:
		return
	vida = max(0.0, vida - cantidad)
	if vida <= 0.0:
		_morir()

func _morir():
	# Demo: reinicia vida (evita game-over duro en el sandbox)
	vida = MAX_VIDA

func recargar_full():
	balas = MAX_BALAS

func get_ammo() -> int:
	return balas

func get_health() -> float:
	return vida

func get_health_percent() -> float:
	return vida / MAX_VIDA

func _handle_movement(delta):
	var current_speed = SPRINT_SPEED if Input.is_action_pressed("sprint") else SPEED
	var input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	if direction:
		velocity.x = direction.x * current_speed
		velocity.z = direction.z * current_speed
	else:
		velocity.x = move_toward(velocity.x, 0, current_speed)
		velocity.z = move_toward(velocity.z, 0, current_speed)

	if is_on_floor():
		if Input.is_action_just_pressed("jump"):
			velocity.y = JUMP_VELOCITY
		else:
			velocity.y = 0.0
	else:
		velocity.y -= GRAVITY * delta

func _handle_camera_look(_delta):
	if Input.is_action_just_pressed("ui_cancel"):
		if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		else:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _input(event):
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * MOUSE_SENSITIVITY)
		camera.rotate_x(-event.relative.y * MOUSE_SENSITIVITY)
		camera.rotation.x = clamp(camera.rotation.x, -PI/2, PI/2)

func _handle_camera_bob(delta):
	if velocity.length() > 0.1:
		bob_time += delta * BOB_FREQ
	else:
		bob_time = 0.0

	var bob_offset = sin(bob_time * PI) * BOB_AMP
	camera.position = camera_base_pos + Vector3(0, bob_offset, 0)

func _handle_flashlight_toggle():
	if Input.is_action_just_pressed("toggle_flashlight"):  # F key
		if flashlight_battery > 0:
			flashlight_active = !flashlight_active
			flashlight.visible = flashlight_active
		else:
			flashlight_active = false
			flashlight.visible = false

func _handle_interaction():
	if Input.is_action_just_pressed("interact"):  # E key
		var space_state = get_world_3d().direct_space_state
		var query = PhysicsRayQueryParameters3D.create(
			camera.global_position,
			camera.global_position + camera.global_transform.basis.z * -3.0
		)
		var result = space_state.intersect_ray(query)

		if result and result.collider.has_method("interact"):
			result.collider.interact()

func _on_flashlight_tick():
	if flashlight_active and flashlight_battery > 0:
		flashlight_battery -= 1.0
		if flashlight_battery <= 0:
			flashlight_battery = 0
			flashlight_active = false
			flashlight.visible = false

func add_battery(amount: float):
	flashlight_battery = min(flashlight_battery + amount, FLASHLIGHT_BATTERY_MAX)
	if flashlight_battery > 0 and not flashlight_active:
		flashlight_active = true
		flashlight.visible = true

func get_battery_percent() -> float:
	return flashlight_battery / FLASHLIGHT_BATTERY_MAX

func get_interaction_prompt() -> String:
	if camera == null:
		return ""
	var space_state = get_world_3d().direct_space_state
	var query = PhysicsRayQueryParameters3D.create(
		camera.global_position,
		camera.global_position + camera.global_transform.basis.z * -3.0
	)
	var result = space_state.intersect_ray(query)
	if result and result.collider.has_method("interact"):
		return "[E] Interactuar"
	return ""
