extends Node3D

# Zonas de activación de eventos (posición Z del jugador)
# Ajustadas a la nueva geometría v2:
#   Mezzanine: Z=8..28, Escaleras: Z=30..48, Andén: Z=48..128
const ZONA_FALLO_MEZZ_1 = 15.0     # Entrando al mezzanine
const ZONA_FALLO_MEZZ_2 = 25.0     # Pasando los torniquetes
const ZONA_FALLO_ESCALERA = 38.0   # Bajando escaleras al andén
const ZONA_FALLO_ANDEN_1 = 60.0    # Caminando por el andén (primera luz)
const ZONA_FALLO_ANDEN_2 = 80.0    # Caminando por el andén (segunda luz)
const ZONA_COLA_MANIOBRAS = 52.0   # Cerca de la reja norte (cola de maniobras)
const ZONA_SALA_CONTROL = 120.0    # Cerca de la cabina de control sur

@onready var player: Node3D = get_node_or_null("Player")
@onready var iluminacion: Node3D = get_node_or_null("Iluminacion")

var luz_mezz_1: OmniLight3D
var luz_mezz_2: OmniLight3D
var luz_mezz_3: OmniLight3D
var luz_esc_1: OmniLight3D
var luz_anden_1: OmniLight3D
var luz_anden_2: OmniLight3D
var luz_anden_3: OmniLight3D

var falladas := {}
var cola_maniobras_disparada := false
var sala_control_disparada := false
var zumbido_iniciado := false

func _ready() -> void:
	# Vincular las luces de la escena
	if iluminacion:
		luz_mezz_1 = iluminacion.get_node_or_null("Luz_Mezzanine_01")
		luz_mezz_2 = iluminacion.get_node_or_null("Luz_Mezzanine_02")
		luz_mezz_3 = iluminacion.get_node_or_null("Luz_Mezzanine_03")
		luz_esc_1 = iluminacion.get_node_or_null("Luz_Escalera_01")
		luz_anden_1 = iluminacion.get_node_or_null("Luz_Anden_01")
		luz_anden_2 = iluminacion.get_node_or_null("Luz_Anden_02")
		luz_anden_3 = iluminacion.get_node_or_null("Luz_Anden_03")

	# Iniciar el zumbido de fondo si existe el player
	if has_node("Audio/ZumbidoPlayer"):
		var zumbido = get_node("Audio/ZumbidoPlayer") as AudioStreamPlayer3D
		zumbido.play()
		zumbido_iniciado = true

	# Aplicar texturas PBR realistas a toda la geometría
	_aplicar_materiales_pbr()


func _aplicar_materiales_pbr() -> void:
	var geometria = get_node_or_null("Geometria")
	if not geometria:
		return

	const TEX_PATH = "res://assets/textures/"
	var mat_hormigon = load(TEX_PATH + "hormigon/Concrete034_1K-JPG.tres")
	var mat_azulejo = load(TEX_PATH + "azulejo_rojo/Tiles141_1K-JPG.tres")
	var mat_terrazo = load(TEX_PATH + "terrazo_piso/Terrazzo013_1K-JPG.tres")
	var mat_metal = load(TEX_PATH + "metal_oxidado/Metal063_1K-JPG.tres")
	var mat_balasto = load(TEX_PATH + "balasto/Gravel043_1K-JPG.tres")

	# Recorrer recursivamente todos los MeshInstance3D
	_aplicar_recursivo(geometria, mat_hormigon, mat_azulejo, mat_terrazo, mat_metal, mat_balasto)


func _aplicar_recursivo(nodo: Node, mat_hormigon, mat_azulejo, mat_terrazo, mat_metal, mat_balasto) -> void:
	if nodo is MeshInstance3D:
		var n = nodo.name.to_lower()
		var mat: Material = null

		# Pisos y rampas → terrazo
		if "piso" in n or "rampa" in n or "descanso" in n and "piso" in n:
			mat = mat_terrazo
		# Franjas de seguridad → no cambiar (mantener amarillo)
		elif "franja" in n:
			pass
		# Rieles → no cambiar (mantener metal de riel)
		elif "riel" in n:
			pass
		# Muros → azulejo rojo (estilo metro Santiago)
		elif "muro" in n:
			mat = mat_azulejo
		# Foso de vías → balasto/grava
		elif "foso" in n or "balasto" in n:
			mat = mat_balasto
		# Techos, vigas → metal
		elif "techo" in n or "viga" in n:
			mat = mat_metal
		# Props metálicos
		elif "boleteria" in n or "torniquetes" in n or "reja" in n or "sala_control" in n or "banca" in n:
			mat = mat_metal
		# Columnas → hormigón
		elif "columna" in n:
			mat = mat_hormigon
		# Bordes del andén → hormigón
		elif "borde" in n:
			mat = mat_hormigon
		# Calle/plaza → hormigón
		elif "calle" in n or "plaza" in n:
			mat = mat_hormigon
		# Default → hormigón
		else:
			mat = mat_hormigon

		if mat:
			nodo.set_surface_override_material(0, mat)

	# Recorrer hijos recursivamente
	for child in nodo.get_children():
		_aplicar_recursivo(child, mat_hormigon, mat_azulejo, mat_terrazo, mat_metal, mat_balasto)


func _process(_delta: float) -> void:
	if not player:
		return

	var pz = player.position.z

	# --- Control de Fallo de Luces según Z ---
	if pz > ZONA_FALLO_MEZZ_1 and not falladas.has(luz_mezz_1):
		_fallar_luz(luz_mezz_1)

	if pz > ZONA_FALLO_MEZZ_2 and not falladas.has(luz_mezz_2):
		_fallar_luz(luz_mezz_2)
		_fallar_luz(luz_mezz_3)

	if pz > ZONA_FALLO_ESCALERA and not falladas.has(luz_esc_1):
		_fallar_luz(luz_esc_1)

	if pz > ZONA_FALLO_ANDEN_1 and not falladas.has(luz_anden_1):
		_fallar_luz(luz_anden_1)

	if pz > ZONA_FALLO_ANDEN_2 and not falladas.has(luz_anden_2):
		_fallar_luz(luz_anden_2)

	# --- Evento de Cola de Maniobras (Extremo Norte, Z disminuye) ---
	if pz < ZONA_COLA_MANIOBRAS and player.position.y < -6.0:
		if not cola_maniobras_disparada:
			_disparar_cola_maniobras()
	else:
		if cola_maniobras_disparada and pz > ZONA_COLA_MANIOBRAS + 3.0:
			_apagar_cola_maniobras()

	# --- Evento de Sala de Control (Extremo Sur, Z aumenta) ---
	if pz > ZONA_SALA_CONTROL and not sala_control_disparada:
		_disparar_sala_control()


func _fallar_luz(luz: OmniLight3D) -> void:
	if not luz:
		return
	falladas[luz] = true

	# Efecto de parpadeo (flicker) antes de apagarse por completo
	var tween = create_tween()
	var energia_original = luz.light_energy

	# Secuencia de parpadeos rápidos
	tween.tween_property(luz, "light_energy", 0.1, 0.05)
	tween.tween_property(luz, "light_energy", energia_original, 0.05)
	tween.tween_property(luz, "light_energy", 0.0, 0.08)
	tween.tween_property(luz, "light_energy", energia_original * 0.7, 0.05)
	tween.tween_property(luz, "light_energy", 0.0, 0.15).set_trans(Tween.TRANS_EXPO)

	if has_node("Audio/ChisporroteoPlayer"):
		var audio = get_node("Audio/ChisporroteoPlayer") as AudioStreamPlayer3D
		audio.global_position = luz.global_position
		audio.play()


func _disparar_cola_maniobras() -> void:
	cola_maniobras_disparada = true
	print("[Evento] Jugador se acerca a la Cola de Maniobras. Activando susurros.")
	if has_node("Audio/SusurroPlayer"):
		var susurro = get_node("Audio/SusurroPlayer") as AudioStreamPlayer3D
		susurro.play()


func _apagar_cola_maniobras() -> void:
	cola_maniobras_disparada = false
	print("[Evento] Jugador se aleja de la Cola de Maniobras. Apagando susurros.")
	if has_node("Audio/SusurroPlayer"):
		var susurro = get_node("Audio/SusurroPlayer") as AudioStreamPlayer3D
		var tween = create_tween()
		tween.tween_property(susurro, "volume_db", -80.0, 2.0)
		tween.tween_callback(susurro.stop)
		tween.tween_callback(func(): susurro.volume_db = 0.0)


func _disparar_sala_control() -> void:
	sala_control_disparada = true
	print("[Evento] Jugador llega a la Sala de Control. Sonido de impacto lejano.")

	# Sonido de golpe metálico en las tuberías/cabina
	if has_node("Audio/TrenFantasmaPlayer"):
		var audio = get_node("Audio/TrenFantasmaPlayer") as AudioStreamPlayer3D
		audio.global_position = Vector3(0.0, -10.5, 124.0)  # Detrás de la cabina
		audio.play()
