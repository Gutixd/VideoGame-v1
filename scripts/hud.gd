extends CanvasLayer

# HUD minimalista y diegetico-friendly para LINEA CERO:
#  - Punto de mira sutil al centro.
#  - Indicador de bateria de la linterna (abajo-izquierda), se pone rojo
#    y parpadea cuando queda poca.
#  - Aviso de interaccion (abajo-centro) cuando el jugador mira algo usable.
# Lee al jugador por el grupo "player"; no acopla nada mas.

const BAR_W := 180.0
const BAR_H := 12.0
const UMBRAL_BAJO := 0.25

var _player: Node = null
var _bar_bg: ColorRect
var _bar_fill: ColorRect
var _lbl_bateria: Label
var _prompt: Label
var _parpadeo := 0.0

var _vida_bg: ColorRect
var _vida_fill: ColorRect
var _lbl_vida: Label
var _lbl_balas: Label

var _stamina_bg: ColorRect
var _stamina_fill: ColorRect
var _lbl_stamina: Label


func _ready():
	layer = 10
	_construir_crosshair()
	_construir_bateria()
	_construir_vida()
	_construir_stamina()
	_construir_balas()
	_construir_prompt()
	await get_tree().process_frame
	_player = get_tree().get_first_node_in_group("player")


func _construir_vida():
	_lbl_vida = Label.new()
	_lbl_vida.text = "SALUD"
	_lbl_vida.add_theme_font_size_override("font_size", 12)
	_lbl_vida.add_theme_color_override("font_color", Color(0.92, 0.82, 0.82, 0.85))
	_anclar_abajo_izq(_lbl_vida, 26, 132, 160, 16)
	add_child(_lbl_vida)

	_vida_bg = ColorRect.new()
	_vida_bg.color = Color(0, 0, 0, 0.55)
	_anclar_abajo_izq(_vida_bg, 26, 114, BAR_W, BAR_H)
	add_child(_vida_bg)

	_vida_fill = ColorRect.new()
	_vida_fill.color = Color(0.9, 0.25, 0.2, 0.95)
	_vida_fill.anchor_bottom = 1.0
	_vida_fill.offset_left = 2
	_vida_fill.offset_top = 2
	_vida_fill.offset_bottom = -2
	_vida_fill.offset_right = BAR_W - 2
	_vida_bg.add_child(_vida_fill)


func _construir_stamina():
	_lbl_stamina = Label.new()
	_lbl_stamina.text = "RESISTENCIA"
	_lbl_stamina.add_theme_font_size_override("font_size", 12)
	_lbl_stamina.add_theme_color_override("font_color", Color(0.85, 0.9, 0.82, 0.85))
	_anclar_abajo_izq(_lbl_stamina, 26, 88, 160, 16)
	add_child(_lbl_stamina)

	_stamina_bg = ColorRect.new()
	_stamina_bg.color = Color(0, 0, 0, 0.55)
	_anclar_abajo_izq(_stamina_bg, 26, 70, BAR_W, BAR_H)
	add_child(_stamina_bg)

	_stamina_fill = ColorRect.new()
	_stamina_fill.color = Color(0.65, 0.9, 0.55, 0.95)
	_stamina_fill.anchor_bottom = 1.0
	_stamina_fill.offset_left = 2
	_stamina_fill.offset_top = 2
	_stamina_fill.offset_bottom = -2
	_stamina_fill.offset_right = BAR_W - 2
	_stamina_bg.add_child(_stamina_fill)


func _construir_balas():
	_lbl_balas = Label.new()
	_lbl_balas.text = "100"
	_lbl_balas.add_theme_font_size_override("font_size", 34)
	_lbl_balas.add_theme_color_override("font_color", Color(1, 0.95, 0.75, 0.95))
	_lbl_balas.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_lbl_balas.anchor_left = 1.0
	_lbl_balas.anchor_right = 1.0
	_lbl_balas.anchor_top = 1.0
	_lbl_balas.anchor_bottom = 1.0
	_lbl_balas.offset_left = -180
	_lbl_balas.offset_right = -26
	_lbl_balas.offset_top = -78
	_lbl_balas.offset_bottom = -30
	add_child(_lbl_balas)

	var cap := Label.new()
	cap.text = "PISTOLA"
	cap.add_theme_font_size_override("font_size", 12)
	cap.add_theme_color_override("font_color", Color(0.85, 0.82, 0.7, 0.75))
	cap.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	cap.anchor_left = 1.0
	cap.anchor_right = 1.0
	cap.anchor_top = 1.0
	cap.anchor_bottom = 1.0
	cap.offset_left = -180
	cap.offset_right = -26
	cap.offset_top = -96
	cap.offset_bottom = -80
	add_child(cap)


func _construir_crosshair():
	var cc := CenterContainer.new()
	cc.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	cc.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(cc)
	var punto := ColorRect.new()
	punto.color = Color(1, 1, 1, 0.35)
	punto.custom_minimum_size = Vector2(5, 5)
	cc.add_child(punto)


func _anclar_abajo_izq(ctrl: Control, x: float, y_desde_abajo: float, w: float, h: float):
	ctrl.anchor_left = 0.0
	ctrl.anchor_right = 0.0
	ctrl.anchor_top = 1.0
	ctrl.anchor_bottom = 1.0
	ctrl.offset_left = x
	ctrl.offset_right = x + w
	ctrl.offset_top = -y_desde_abajo - h
	ctrl.offset_bottom = -y_desde_abajo


func _construir_bateria():
	_lbl_bateria = Label.new()
	_lbl_bateria.text = "LINTERNA"
	_lbl_bateria.add_theme_font_size_override("font_size", 12)
	_lbl_bateria.add_theme_color_override("font_color", Color(0.82, 0.85, 0.92, 0.85))
	_anclar_abajo_izq(_lbl_bateria, 26, 44, 160, 16)
	add_child(_lbl_bateria)

	_bar_bg = ColorRect.new()
	_bar_bg.color = Color(0, 0, 0, 0.55)
	_anclar_abajo_izq(_bar_bg, 26, 26, BAR_W, BAR_H)
	add_child(_bar_bg)

	_bar_fill = ColorRect.new()
	_bar_fill.color = Color(0.6, 0.85, 1.0, 0.95)
	_bar_fill.anchor_left = 0.0
	_bar_fill.anchor_top = 0.0
	_bar_fill.anchor_right = 0.0
	_bar_fill.anchor_bottom = 1.0
	_bar_fill.offset_left = 2
	_bar_fill.offset_top = 2
	_bar_fill.offset_bottom = -2
	_bar_fill.offset_right = BAR_W - 2
	_bar_bg.add_child(_bar_fill)


func _construir_prompt():
	_prompt = Label.new()
	_prompt.text = ""
	_prompt.add_theme_font_size_override("font_size", 16)
	_prompt.add_theme_color_override("font_color", Color(1, 1, 1, 0.9))
	_prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_prompt.anchor_left = 0.5
	_prompt.anchor_right = 0.5
	_prompt.anchor_top = 1.0
	_prompt.anchor_bottom = 1.0
	_prompt.offset_left = -160
	_prompt.offset_right = 160
	_prompt.offset_top = -96
	_prompt.offset_bottom = -72
	_prompt.visible = false
	add_child(_prompt)


func _process(delta):
	if _player == null or not is_instance_valid(_player):
		_player = get_tree().get_first_node_in_group("player")
		return

	# --- Bateria ---
	if _player.has_method("get_battery_percent"):
		var pct: float = clampf(_player.get_battery_percent(), 0.0, 1.0)
		var ancho := (BAR_W - 4.0) * pct
		_bar_fill.offset_right = 2.0 + ancho
		if pct <= UMBRAL_BAJO:
			_parpadeo += delta * 6.0
			var a := 0.5 + 0.5 * sin(_parpadeo)
			_bar_fill.color = Color(0.95, 0.2, 0.15, a)
		else:
			_bar_fill.color = Color(0.6, 0.85, 1.0, 0.95)

	# --- Salud ---
	if _player.has_method("get_health_percent"):
		var hp: float = clampf(_player.get_health_percent(), 0.0, 1.0)
		_vida_fill.offset_right = 2.0 + (BAR_W - 4.0) * hp
		_lbl_vida.text = "SALUD  %d" % roundi(hp * 100.0)

	# --- Resistencia ---
	if _player.has_method("get_stamina_percent"):
		var sp: float = clampf(_player.get_stamina_percent(), 0.0, 1.0)
		_stamina_fill.offset_right = 2.0 + (BAR_W - 4.0) * sp
		_stamina_fill.color = Color(0.9, 0.3, 0.25, 0.95) if sp <= 0.0 else Color(0.65, 0.9, 0.55, 0.95)

	# --- Balas ---
	if _player.has_method("get_ammo"):
		_lbl_balas.text = str(_player.get_ammo())

	# --- Aviso de interaccion ---
	if _player.has_method("get_interaction_prompt"):
		var txt: String = _player.get_interaction_prompt()
		_prompt.text = txt
		_prompt.visible = txt != ""
