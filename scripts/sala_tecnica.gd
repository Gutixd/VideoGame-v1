extends Node3D

const MAT_AZULEJO = preload("res://assets/textures/azulejo_rojo/Tiles141_1K-JPG.tres")
const MAT_HORMIGON = preload("res://assets/textures/hormigon/Concrete034_1K-JPG.tres")
const MAT_METAL_OXIDADO = preload("res://assets/textures/metal_oxidado/Metal063_1K-JPG.tres")

func _ready():
	_apply_materials()

func _create_piso_cemento() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.45, 0.45, 0.47)
	mat.roughness = 0.9
	mat.metallic = 0.0
	return mat

func _create_puerta_metal() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.12, 0.12, 0.14)
	mat.roughness = 0.5
	mat.metallic = 0.6
	return mat

func _create_azulejo_solido() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.75, 0.12, 0.1)
	mat.roughness = 0.4
	mat.metallic = 0.0
	return mat

func _create_luz_fixture() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.3, 0.05, 0.05)
	mat.emission_enabled = true
	mat.emission = Color(1.0, 0.15, 0.1)
	mat.emission_energy_multiplier = 3.0
	return mat

func _apply_materials():
	if has_node("Piso"):
		$Piso.material = _create_piso_cemento()

	if has_node("Techo"):
		$Techo.material = MAT_HORMIGON

	if has_node("ParedFrente"):
		$ParedFrente.material = MAT_AZULEJO

	if has_node("ParedFondo"):
		$ParedFondo.material = MAT_AZULEJO

	if has_node("ParedIzquierda"):
		$ParedIzquierda.material = MAT_HORMIGON

	if has_node("ParedDerecha"):
		$ParedDerecha.material = MAT_HORMIGON

	if has_node("Puerta"):
		$Puerta.material = _create_puerta_metal()

	if has_node("Tuberias"):
		for tuberia in $Tuberias.get_children():
			tuberia.material = MAT_METAL_OXIDADO

	if has_node("Carteles"):
		for cartel in $Carteles.get_children():
			if cartel.has_node("Panel"):
				cartel.get_node("Panel").material = _create_azulejo_solido()

	if has_node("Luces_Emergencia"):
		for fixture in $Luces_Emergencia.get_children():
			if fixture is CSGSphere3D:
				fixture.material = _create_luz_fixture()
