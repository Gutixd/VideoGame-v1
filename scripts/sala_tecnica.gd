extends Node3D

func _ready():
	_apply_materials()

func _create_azulejo_rojo() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.75, 0.12, 0.1)
	mat.roughness = 0.4
	mat.metallic = 0.0
	return mat

func _create_hormigon() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.6, 0.6, 0.6)
	mat.roughness = 0.8
	mat.metallic = 0.0
	return mat

func _create_metal_oxidado() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.5, 0.4, 0.32)
	mat.roughness = 0.6
	mat.metallic = 0.7
	return mat

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
		$Techo.material = _create_hormigon()

	if has_node("ParedFrente"):
		$ParedFrente.material = _create_azulejo_rojo()

	if has_node("ParedFondo"):
		$ParedFondo.material = _create_azulejo_rojo()

	if has_node("ParedIzquierda"):
		$ParedIzquierda.material = _create_hormigon()

	if has_node("ParedDerecha"):
		$ParedDerecha.material = _create_hormigon()

	if has_node("Puerta"):
		$Puerta.material = _create_puerta_metal()

	if has_node("Tuberias"):
		for tuberia in $Tuberias.get_children():
			tuberia.material = _create_metal_oxidado()

	if has_node("Carteles"):
		for cartel in $Carteles.get_children():
			if cartel.has_node("Panel"):
				cartel.get_node("Panel").material = _create_azulejo_rojo()

	if has_node("Luces_Emergencia"):
		for fixture in $Luces_Emergencia.get_children():
			if fixture is CSGSphere3D:
				fixture.material = _create_luz_fixture()
