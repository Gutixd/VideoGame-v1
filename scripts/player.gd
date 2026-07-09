extends CharacterBody3D

const SPEED = 4.5
const MOUSE_SENSITIVITY = 0.003
const BOB_FREQ = 2.0
const BOB_AMP = 0.08
const FLASHLIGHT_BATTERY_MAX = 180.0

@onready var camera = $Camera3D
@onready var flashlight = $Camera3D/SpotLight3D
@onready var flashlight_timer = $FlashlightTimer

var bob_time = 0.0
var camera_base_pos: Vector3
var flashlight_battery = FLASHLIGHT_BATTERY_MAX
var flashlight_active = true

func _ready():
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

	move_and_slide()

func _handle_movement(delta):
	var input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	if direction:
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		velocity.z = move_toward(velocity.z, 0, SPEED)

	if is_on_floor():
		velocity.y = 0.0
	else:
		velocity.y -= 9.8 * delta

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
