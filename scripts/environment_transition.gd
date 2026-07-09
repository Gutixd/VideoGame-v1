extends Area3D

@export var world_environment_path: NodePath
@export var ambient_color_destino: Color = Color(0.15, 0.16, 0.18)
@export var ambient_energy_destino: float = 0.3
@export var background_color_destino: Color = Color(0.015, 0.015, 0.018)
@export var duracion: float = 3.0

var _ya_disparado := false

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node3D) -> void:
	if _ya_disparado:
		return
	if not body.is_in_group("player"):
		return
	_ya_disparado = true
	_transicionar()

func _transicionar() -> void:
	var world_env := get_node_or_null(world_environment_path) as WorldEnvironment
	if not world_env or not world_env.environment:
		return
	var env := world_env.environment
	var tween := create_tween()
	tween.set_parallel(true)
	tween.tween_property(env, "ambient_light_color", ambient_color_destino, duracion)
	tween.tween_property(env, "ambient_light_energy", ambient_energy_destino, duracion)
	tween.tween_property(env, "background_color", background_color_destino, duracion)
