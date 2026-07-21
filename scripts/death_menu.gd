extends CanvasLayer

const ESCENA_MENU_PRINCIPAL := "res://scenes/main_menu.tscn"

var _panel: Control


func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	layer = 20
	_construir_ui()
	_panel.visible = false


func _construir_ui():
	_panel = Control.new()
	_panel.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_panel)

	var fondo := ColorRect.new()
	fondo.color = Color(0.02, 0, 0, 0.85)
	fondo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_panel.add_child(fondo)

	var titulo := Label.new()
	titulo.text = "HAS MUERTO"
	titulo.add_theme_font_size_override("font_size", 48)
	titulo.add_theme_color_override("font_color", Color(0.85, 0.12, 0.1, 1.0))
	titulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_anclar_centrado_x(titulo, 0.34, -260, 260, -35, 35)
	_panel.add_child(titulo)

	var reaparecer := Button.new()
	reaparecer.text = "REAPARECER"
	reaparecer.add_theme_font_size_override("font_size", 22)
	_anclar_centrado_x(reaparecer, 0.5, -120, 120, 0, 50)
	reaparecer.pressed.connect(_on_reaparecer_pressed)
	_panel.add_child(reaparecer)

	var menu := Button.new()
	menu.text = "MENÚ PRINCIPAL"
	menu.add_theme_font_size_override("font_size", 18)
	_anclar_centrado_x(menu, 0.6, -120, 120, 0, 46)
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


func mostrar():
	_panel.visible = true
	get_tree().paused = true
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)


func _on_reaparecer_pressed():
	_panel.visible = false
	get_tree().paused = false
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	var jugador = get_tree().get_first_node_in_group("player")
	if jugador and jugador.has_method("respawn"):
		jugador.respawn()


func _on_menu_pressed():
	get_tree().paused = false
	get_tree().change_scene_to_file(ESCENA_MENU_PRINCIPAL)
