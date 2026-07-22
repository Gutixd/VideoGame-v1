extends Node3D
## Demo: el tren llega al anden, abre puertas, el jugador entra y las puertas se cierran.

const ENTRY_X       := 17.3    # puerta del coche del medio (donde esta el interior)
const TRAIN_START_X := 78.0    # desde donde entra el tren
const DOOR_SLIDE    := 1.35    # cuanto corre cada hoja de puerta
const FLOOR_Y       := 1.36    # altura del piso interior del tren
const ARRIVAL_TIME  := 30.0

var train: Node3D
var door_nodes: Array[Node3D] = []
var door_base_x: Array[float] = []
var hud: Label
var player: CharacterBody3D
var doors_open := false
var sequence_done := false


func _ready() -> void:
	_build_environment()
	_load_model()
	_build_platform()
	if train:
		_collect_doors()
		_build_train_floor()
		_build_pared_tren()
		_build_entry_area()
	_build_lights()
	_build_player()
	_build_hud()
	_start_sequence()


# ---------------------------------------------------------------- utilidades
func _find(node: Node, target: String) -> Node:
	if node.name == target:
		return node
	for c in node.get_children():
		var r: Node = _find(c, target)
		if r != null:
			return r
	return null


func _collect(node: Node, out: Array) -> void:
	out.append(node)
	for c in node.get_children():
		_collect(c, out)


func _mat(color: Color, emissive := false) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	m.roughness = 0.7
	if emissive:
		m.emission_enabled = true
		m.emission = color
		m.emission_energy_multiplier = 1.5
	return m


func _box(parent: Node, nm: String, size: Vector3, pos: Vector3, color: Color,
		  with_body := true, emissive := false, collision_layer := 1) -> Node3D:
	var holder := Node3D.new()
	holder.name = nm
	holder.position = pos
	parent.add_child(holder)

	var mi := MeshInstance3D.new()
	var bm := BoxMesh.new()
	bm.size = size
	mi.mesh = bm
	mi.material_override = _mat(color, emissive)
	holder.add_child(mi)

	if with_body:
		var sb := StaticBody3D.new()
		sb.collision_layer = collision_layer
		sb.collision_mask = 0
		var cs := CollisionShape3D.new()
		var shape := BoxShape3D.new()
		shape.size = size
		cs.shape = shape
		sb.add_child(cs)
		holder.add_child(sb)
	return holder


# ---------------------------------------------------------------- construccion
func _build_environment() -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.015, 0.015, 0.02)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.55, 0.55, 0.6)
	env.ambient_light_energy = 0.55
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)


func _load_model() -> void:
	var packed: Resource = load("res://assets/models/tren/metro.glb")
	if packed == null:
		push_error("No se pudo cargar res://assets/models/tren/metro.glb")
		return
	var scene: Node = packed.instantiate()
	scene.name = "MetroModelo"
	add_child(scene)
	train = _find(scene, "Tren_Root") as Node3D
	if train == null:
		push_warning("No se encontro 'Tren_Root' en el GLB; el tren no se movera.")


func _collect_doors() -> void:
	var todos: Array = []
	_collect(train, todos)
	for n in todos:
		if n is Node3D and String(n.name).begins_with("Puerta"):
			var n3 := n as Node3D
			# solo las del lado del anden (Z positivo tras la conversion glTF)
			if n3.position.z > 0.5:
				door_nodes.append(n3)
				door_base_x.append(n3.position.x)
				_agregar_colision_puerta(n3)
	print("Puertas encontradas (lado anden): ", door_nodes.size())


func _agregar_colision_puerta(puerta: Node3D) -> void:
	# Colision pegada a la puerta misma (hija de ella): al abrirse/cerrarse
	# con el tween, la colision se mueve exactamente igual que la hoja
	# visible -- bloquea el paso cuando esta cerrada, se despeja cuando se
	# desliza abierta. El .glb no trae colision propia, hay que crearla.
	_colision_invisible(puerta, Vector3(1.40, 1.85, 0.05), Vector3.ZERO)


func _colision_invisible(parent: Node, size: Vector3, pos: Vector3) -> void:
	# Solo fisica, sin malla visible (el modelo del tren ya tiene su propia
	# pared visual en el .glb -- si aca se dibujara otra caja encima quedaria
	# parpadeando/duplicada sobre la misma superficie).
	var sb := StaticBody3D.new()
	sb.position = pos
	sb.collision_layer = 1
	sb.collision_mask = 0
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size
	cs.shape = shape
	sb.add_child(cs)
	parent.add_child(sb)


func _build_platform() -> void:
	# Losa del anden: nivelada con el piso del tren y pegada al costado del tren.
	_box(self, "Anden", Vector3(140, 0.3, 7.0), Vector3(12, FLOOR_Y - 0.15, 4.8),
		 Color(0.72, 0.70, 0.66))
	# Linea amarilla de seguridad
	_box(self, "LineaAmarilla", Vector3(140, 0.02, 0.4), Vector3(12, FLOOR_Y + 0.01, 2.6),
		 Color(0.95, 0.76, 0.05), false, true)
	# Piso de la via (bajo el tren): el modelo del .glb es solo visual, sin
	# colision fisica -- sin esto el jugador atraviesa el piso bajo el metro
	# y cae al vacio. Queda mas abajo que el anden, como el desnivel real.
	_box(self, "Via", Vector3(140, 0.2, 5.0), Vector3(12, FLOOR_Y - 0.9, -0.2),
		 Color(0.05, 0.05, 0.06))
	# Muro trasero del anden (lado contrario a la via): igual que la via,
	# en el .glb es solo visual -- sin colision el jugador caminaba hasta
	# el borde de atras y se caia. Bloquea el paso ahi.
	_box(self, "MuroAnden", Vector3(140, 3.0, 0.3), Vector3(12, FLOOR_Y + 1.35, 8.35),
		 Color(0.75, 0.72, 0.68))
	# Muro del otro lado de la via (detras del tren): tambien solo visual
	# en el .glb, se completa aca.
	_box(self, "MuroLejano", Vector3(140, 6.0, 0.3), Vector3(12, FLOOR_Y + 2.85, -3.0),
		 Color(0.64, 0.56, 0.44))
	# Techo del tunel/anden. Capa 2: para que el raycast de "aparecer sobre
	# el piso" (capa 1 solamente) no lo confunda con el suelo real.
	_box(self, "Techo", Vector3(140, 0.4, 14.0), Vector3(12, FLOOR_Y + 6.9, 1.0),
		 Color(0.03, 0.03, 0.035), true, false, 2)


func _build_pared_tren() -> void:
	# Colision del costado del tren que da al anden: solida entre puertas,
	# con un hueco exacto en cada puerta para poder entrar. El .glb del
	# tren no trae colision propia -- antes se podia atravesar el costado
	# entero del vagon por cualquier parte, no solo por las puertas.
	if door_base_x.is_empty():
		return
	var z_pared: float = door_nodes[0].position.z
	var xs: Array = door_base_x.duplicate()
	xs.sort()
	var unicos: Array = []
	for x in xs:
		if unicos.is_empty() or x - unicos[-1] > 0.3:
			unicos.append(x)
	var ancho_hueco := 1.6
	for i in range(unicos.size() - 1):
		var izq: float = unicos[i] + ancho_hueco / 2.0
		var der: float = unicos[i + 1] - ancho_hueco / 2.0
		var ancho: float = der - izq
		if ancho <= 0.1:
			continue
		var centro: float = (izq + der) / 2.0
		_colision_invisible(train, Vector3(ancho, 1.85, 0.05), Vector3(centro, 2.2, z_pared))
	# Tapas en los extremos, antes de la primera puerta y despues de la ultima.
	_colision_invisible(train, Vector3(2.0, 1.85, 0.05),
		 Vector3(unicos[0] - ancho_hueco / 2.0 - 1.0, 2.2, z_pared))
	_colision_invisible(train, Vector3(2.0, 1.85, 0.05),
		 Vector3(unicos[-1] + ancho_hueco / 2.0 + 1.0, 2.2, z_pared))
	# Mampara de la cabina (coche lider): solo tenia malla visual, sin
	# colision se podia atravesar y entrar caminando a la cabina.
	_colision_invisible(train, Vector3(0.15, 2.10, 2.50), Vector3(39.9, 2.30, 0))


func _build_train_floor() -> void:
	# Piso interior del tren (hijo del tren, se mueve con el)
	_box(train, "PisoTren", Vector3(54, 0.2, 2.3), Vector3(17.3, FLOOR_Y - 0.1, 0),
		 Color(0.6, 0.6, 0.62))


func _build_entry_area() -> void:
	var area := Area3D.new()
	area.name = "ZonaEntrada"
	area.position = Vector3(ENTRY_X, FLOOR_Y + 0.9, 0)
	var cs := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = Vector3(5.0, 1.8, 1.9)
	cs.shape = shape
	area.add_child(cs)
	train.add_child(area)
	area.body_entered.connect(_on_player_entered)


func _build_lights() -> void:
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-55, -35, 0)
	sun.light_energy = 0.25
	add_child(sun)

	for x in [-20, 0, 17, 34, 50]:
		var l := OmniLight3D.new()
		l.position = Vector3(x, 5.2, 4.0)
		l.light_energy = 4.0
		l.omni_range = 32.0
		add_child(l)

	# luz dentro del coche de entrada
	if train:
		var li := OmniLight3D.new()
		li.position = Vector3(ENTRY_X, 3.0, 0)
		li.light_energy = 3.0
		li.omni_range = 14.0
		train.add_child(li)


func _build_player() -> void:
	# Jugador completo (salto, gravedad, stamina, vida, linterna, HUD, pausa, muerte)
	var player_scene: PackedScene = load("res://blender_pipeline/METRO_BAQUEDANO_H/player.tscn")
	player = player_scene.instantiate()
	# parado en el anden, mirando hacia el tren (-Z); el propio player.gd se
	# autoajusta al piso real con un raycast apenas entra en la escena.
	player.position = Vector3(ENTRY_X, FLOOR_Y + 1.0, 5.2)
	add_child(player)


func _build_hud() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)
	hud = Label.new()
	hud.position = Vector2(24, 20)
	hud.add_theme_font_size_override("font_size", 20)
	hud.add_theme_color_override("font_color", Color(1, 1, 1))
	hud.add_theme_color_override("font_outline_color", Color(0, 0, 0))
	hud.add_theme_constant_override("outline_size", 6)
	layer.add_child(hud)
	_say("El tren esta llegando...")


func _say(t: String) -> void:
	if hud:
		hud.text = t + "\n\n[WASD] moverse   [Mouse] mirar   [Shift] correr   [Espacio] saltar   [R] reiniciar   [ESC] pausa"


func _input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_R:
			# reinicia toda la escena: el tren vuelve a llegar desde el tunel
			Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
			get_tree().reload_current_scene()


# ---------------------------------------------------------------- secuencia
func _start_sequence() -> void:
	if train == null:
		_say("ERROR: no se encontro el tren en el modelo.")
		return
	train.position.x = TRAIN_START_X
	var t := create_tween()
	t.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	t.tween_property(train, "position:x", 0.0, ARRIVAL_TIME)
	t.finished.connect(_on_train_arrived)


func _on_train_arrived() -> void:
	_say("Tren detenido. Abriendo puertas...")
	await get_tree().create_timer(0.6).timeout
	_open_doors()


func _open_doors() -> void:
	if door_nodes.is_empty():
		_say("Puertas abiertas (no se hallaron hojas para animar). Sube al tren.")
		doors_open = true
		return
	var t := create_tween()
	t.set_parallel(true)
	t.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
	for i in door_nodes.size():
		t.tween_property(door_nodes[i], "position:x", door_base_x[i] + DOOR_SLIDE, 1.1)
	await t.finished
	doors_open = true
	_say("Puertas abiertas - sube al tren")


func _on_player_entered(body: Node) -> void:
	if sequence_done or not doors_open:
		return
	if body != player:
		return
	sequence_done = true
	_say("Entraste al tren. Cerrando puertas...")
	await get_tree().create_timer(1.0).timeout
	_close_doors()


func _close_doors() -> void:
	var t := create_tween()
	t.set_parallel(true)
	t.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
	for i in door_nodes.size():
		t.tween_property(door_nodes[i], "position:x", door_base_x[i], 1.1)
	await t.finished
	doors_open = false
	_say("Puertas cerradas. Proxima estacion: Los Heroes")
