extends CanvasLayer

# 4ta interfaz: INVENTARIO para guardar cosas.
# Se abre/cierra con la accion "inventory" (tecla Tab). Al abrir libera el
# mouse; al cerrar lo vuelve a capturar. Rejilla de ranuras; agregar_item()
# guarda un objeto en la primera ranura libre.

const FILAS := 3
const COLS := 4
const SLOTS := FILAS * COLS

var _abierto := false
var _fondo: ColorRect
var _panel: PanelContainer
var _grid: GridContainer
var _ranuras: Array = []      # Labels de cada ranura
var _items: Array = []        # nombres guardados


func _ready():
	layer = 30
	_construir()
	visible = false
	# Items de ejemplo para que se vea que funciona
	agregar_item("Llave maestra")
	agregar_item("Bateria")
	agregar_item("Nota")


func _construir():
	_fondo = ColorRect.new()
	_fondo.color = Color(0, 0, 0, 0.6)
	_fondo.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_fondo.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_fondo)

	var centro := CenterContainer.new()
	centro.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	centro.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(centro)

	var vbox := VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 12)
	centro.add_child(vbox)

	var titulo := Label.new()
	titulo.text = "INVENTARIO"
	titulo.add_theme_font_size_override("font_size", 24)
	titulo.add_theme_color_override("font_color", Color(0.95, 0.95, 1.0))
	titulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(titulo)

	_panel = PanelContainer.new()
	vbox.add_child(_panel)

	var margen := MarginContainer.new()
	for m in ["margin_left", "margin_right", "margin_top", "margin_bottom"]:
		margen.add_theme_constant_override(m, 16)
	_panel.add_child(margen)

	_grid = GridContainer.new()
	_grid.columns = COLS
	_grid.add_theme_constant_override("h_separation", 10)
	_grid.add_theme_constant_override("v_separation", 10)
	margen.add_child(_grid)

	for i in range(SLOTS):
		var ranura := Panel.new()
		ranura.custom_minimum_size = Vector2(96, 96)
		var etq := Label.new()
		etq.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		etq.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		etq.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		etq.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		etq.add_theme_font_size_override("font_size", 13)
		etq.text = ""
		ranura.add_child(etq)
		_grid.add_child(ranura)
		_ranuras.append(etq)

	var ayuda := Label.new()
	ayuda.text = "Tab para cerrar"
	ayuda.add_theme_font_size_override("font_size", 13)
	ayuda.add_theme_color_override("font_color", Color(0.8, 0.8, 0.85, 0.7))
	ayuda.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(ayuda)


func _unhandled_input(event):
	if event.is_action_pressed("inventory"):
		_toggle()
		get_viewport().set_input_as_handled()


func _toggle():
	_abierto = not _abierto
	visible = _abierto
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE if _abierto else Input.MOUSE_MODE_CAPTURED)


func agregar_item(nombre: String) -> bool:
	if _items.size() >= SLOTS:
		return false
	_items.append(nombre)
	_refrescar()
	return true


func _refrescar():
	for i in range(_ranuras.size()):
		_ranuras[i].text = _items[i] if i < _items.size() else ""
