extends Node3D

func _ready():
	_apply_materials()

func _create_azulejo_rojo() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.8, 0.15, 0.1)
	mat.roughness = 0.4
	mat.metallic = 0.0
	return mat

func _create_hormigon() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.65, 0.65, 0.65)
	mat.roughness = 0.8
	mat.metallic = 0.0
	return mat

func _create_metal_oxidado() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.55, 0.45, 0.35)
	mat.roughness = 0.6
	mat.metallic = 0.7
	return mat

func _create_piso_cemento() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.5, 0.5, 0.52)
	mat.roughness = 0.9
	mat.metallic = 0.0
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

	if has_node("Tuberias"):
		for tuberia in $Tuberias.get_children():
			tuberia.material = _create_metal_oxidado()

	if has_node("Carteles"):
		for cartel in $Carteles.get_children():
			cartel.material = _create_azulejo_rojo()
