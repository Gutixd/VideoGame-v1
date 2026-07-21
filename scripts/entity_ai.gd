extends CharacterBody3D

@onready var nav_agent: NavigationAgent3D = $NavigationAgent3D
@onready var audio_player: AudioStreamPlayer3D = $AudioStreamPlayer3D

const SPEED = 5.0
const CATCH_DISTANCE = 1.5

enum State { PATROL, LISTEN, CHASE }
var current_state = State.PATROL
var target_player: Node3D = null

func _ready():
	# Buscar al jugador en la escena
	var players = get_tree().get_nodes_in_group("player")
	if players.size() > 0:
		target_player = players[0]
	
	nav_agent.path_desired_distance = 0.5
	nav_agent.target_desired_distance = CATCH_DISTANCE

func _physics_process(delta):
	if target_player == null:
		return
		
	_update_state()
	
	match current_state:
		State.PATROL:
			_patrol_logic(delta)
		State.LISTEN:
			_listen_logic(delta)
		State.CHASE:
			_chase_logic(delta)
			
	move_and_slide()

func _update_state():
	# Lógica simplificada: si la linterna está prendida o el jugador está muy cerca, perseguir
	if _can_see_player() or _can_hear_player():
		if current_state != State.CHASE:
			current_state = State.CHASE
			# Reproducir sonido perturbador
			if not audio_player.playing:
				audio_player.play()
	else:
		if current_state == State.CHASE:
			current_state = State.LISTEN

func _can_see_player() -> bool:
	if not target_player: return false
	# Verificar si el jugador tiene la linterna prendida (asumimos que la variable flashlight_active existe en player)
	if target_player.has_method("get_battery_percent") and target_player.flashlight_active:
		# En un juego real, haríamos un RayCast para línea de visión
		var dist = global_position.distance_to(target_player.global_position)
		if dist < 40.0: # Alcance visual en la oscuridad
			return true
	return false

func _can_hear_player() -> bool:
	if not target_player: return false
	# Detectar si el jugador se mueve rápido (ruido)
	if target_player.velocity.length() > 2.0:
		var dist = global_position.distance_to(target_player.global_position)
		if dist < 15.0:
			return true
	return false

func _patrol_logic(delta):
	# En modo patrulla, moverse lentamente o quedarse quieto
	velocity = Vector3.ZERO

func _listen_logic(delta):
	# Quedarse quieto escuchando
	velocity = Vector3.ZERO
	# Si pasa el tiempo, volver a patrulla (simplificado)

func _chase_logic(delta):
	nav_agent.target_position = target_player.global_position
	
	if nav_agent.is_navigation_finished():
		return
		
	var current_agent_position: Vector3 = global_position
	var next_path_position: Vector3 = nav_agent.get_next_path_position()
	
	var new_velocity: Vector3 = next_path_position - current_agent_position
	new_velocity = new_velocity.normalized()
	new_velocity = new_velocity * SPEED
	
	velocity = new_velocity
	
	if global_position.distance_to(target_player.global_position) < CATCH_DISTANCE:
		_catch_player()

func _catch_player():
	print("ENTIDAD: Te atrapé!")
	# Llamar al game manager para reiniciar
	if get_tree().root.has_node("GameManager"):
		get_tree().root.get_node("GameManager").trigger_game_over()
	else:
		# Fallback: recargar escena
		get_tree().reload_current_scene()
