extends Node3D

func _ready():
	_apply_materials()

func _apply_materials():
	# Cargar script de materiales
	var materials = load("res://scripts/materials.gd")

	# Aplicar materiales a los nodos CSG
	if has_node("Piso"):
		$Piso.material = materials.create_piso_cemento()

	if has_node("Techo"):
		$Techo.material = materials.create_hormigon()

	if has_node("ParedFrente"):
		$ParedFrente.material = materials.create_azulejo_rojo()

	if has_node("ParedFondo"):
		$ParedFondo.material = materials.create_azulejo_rojo()

	if has_node("ParedIzquierda"):
		$ParedIzquierda.material = materials.create_hormigon()

	if has_node("ParedDerecha"):
		$ParedDerecha.material = materials.create_hormigon()

	# Aplicar metal oxidado a tuberías
	if has_node("Tuberias"):
		for tuberia in $Tuberias.get_children():
			tuberia.material = materials.create_metal_oxidado()

	# Aplicar rojo a carteles
	if has_node("Carteles"):
		for cartel in $Carteles.get_children():
			cartel.material = materials.create_azulejo_rojo()
