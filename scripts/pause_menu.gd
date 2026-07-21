extends CanvasLayer

const ESCENA_MENU_PRINCIPAL := "res://scenes/main_menu.tscn"

var _panel: Control
var _pausado := false


func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	layer = 15
	_construir_ui()


func _construir_ui():
	_panel = Control.new()
	_panel.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	_panel.visible = false
	add_child(_panel)

	var fondo := ColorRect.new()
	fondo.color = Color(0, 0, 0, 0.75)
	fondo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_panel.add_child(fondo)

	var titulo := Label.new()
	titulo.text = "PAUSA"
	titulo.add_theme_font_size_override("font_size", 42)
	titulo.add_theme_color_override("font_color", Color(0.9, 0.9, 0.92, 0.95))
	titulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_anclar_centrado_x(titulo, 0.28, -200, 200, -30, 30)
	_panel.add_child(titulo)

	var reanudar := Button.new()
	reanudar.text = "REANUDAR"
	reanudar.add_theme_font_size_override("font_size", 20)
	_anclar_centrado_x(reanudar, 0.44, -120, 120, 0, 48)
	reanudar.pressed.connect(_reanudar)
	_panel.add_child(reanudar)

	var reaparecer := Button.new()
	reaparecer.text = "REAPARECER"
	reaparecer.add_theme_font_size_override("font_size", 20)
	_anclar_centrado_x(reaparecer, 0.54, -120, 120, 0, 48)
	reaparecer.pressed.connect(_on_reaparecer_pressed)
	_panel.add_child(reaparecer)

	var menu := Button.new()
	menu.text = "MENÚ PRINCIPAL"
	menu.add_theme_font_size_override("font_size", 18)
	_anclar_centrado_x(menu, 0.64, -120, 120, 0, 44)
	menu.pressed.connect(_on_menu_pressed)
	_panel.add_child(menu)


func _anclar_centrado_x(ctrl: Control, y_ratio: float, left: float, right: float, top: float, bottom: float):
	ctrl.anchor_left = 0.5
	ctrl.anchor_right = 0.5
	ctrl.anchor_top = y_ratio
	ctrl.anchor_bottom = y_ratio
	ctrl.offset_left = left
	ctrl.offset_right = right
	ctrl.offset_top = top
	ctrl.offset_bottom = bottom


func _unhandled_input(event):
	if event.is_action_pressed("ui_cancel"):
		if _pausado:
			_reanudar()
		else:
			_pausar()


func _pausar():
	_pausado = true
	_panel.visible = true
	get_tree().paused = true
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)


func _reanudar():
	_pausado = false
	_panel.visible = false
	get_tree().paused = false
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)


func _on_reaparecer_pressed():
	var jugador = get_tree().get_first_node_in_group("player")
	if jugador and jugador.has_method("respawn"):
		jugador.respawn()
	_reanudar()


func _on_menu_pressed():
	get_tree().paused = false
	get_tree().change_scene_to_file(ESCENA_MENU_PRINCIPAL)
