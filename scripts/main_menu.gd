extends CanvasLayer

const ESCENA_JUEGO := "res://scenes/metro_baquedano_h.tscn"


func _ready():
	layer = 10
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	_construir_fondo()
	_construir_titulo()
	_construir_botones()


func _construir_fondo():
	var fondo := ColorRect.new()
	fondo.color = Color(0.01, 0.01, 0.012, 1.0)
	fondo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(fondo)


func _construir_titulo():
	var titulo := Label.new()
	titulo.text = "LÍNEA CERO"
	titulo.add_theme_font_size_override("font_size", 64)
	titulo.add_theme_color_override("font_color", Color(0.82, 0.14, 0.12, 1.0))
	titulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_anclar_centrado_x(titulo, 0.3, -320, 320, -40, 40)
	add_child(titulo)

	var subtitulo := Label.new()
	subtitulo.text = "Metro de Santiago — Estación Baquedano"
	subtitulo.add_theme_font_size_override("font_size", 16)
	subtitulo.add_theme_color_override("font_color", Color(0.7, 0.7, 0.72, 0.8))
	subtitulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_anclar_centrado_x(subtitulo, 0.37, -320, 320, 0, 24)
	add_child(subtitulo)


func _construir_botones():
	var jugar := Button.new()
	jugar.text = "JUGAR"
	jugar.add_theme_font_size_override("font_size", 22)
	_anclar_centrado_x(jugar, 0.55, -120, 120, 0, 52)
	jugar.pressed.connect(_on_jugar_pressed)
	add_child(jugar)

	var salir := Button.new()
	salir.text = "SALIR"
	salir.add_theme_font_size_override("font_size", 18)
	_anclar_centrado_x(salir, 0.67, -120, 120, 0, 46)
	salir.pressed.connect(_on_salir_pressed)
	add_child(salir)


func _anclar_centrado_x(ctrl: Control, y_ratio: float, left: float, right: float, top: float, bottom: float):
	ctrl.anchor_left = 0.5
	ctrl.anchor_right = 0.5
	ctrl.anchor_top = y_ratio
	ctrl.anchor_bottom = y_ratio
	ctrl.offset_left = left
	ctrl.offset_right = right
	ctrl.offset_top = top
	ctrl.offset_bottom = bottom


func _on_jugar_pressed():
	get_tree().change_scene_to_file(ESCENA_JUEGO)


func _on_salir_pressed():
	get_tree().quit()
