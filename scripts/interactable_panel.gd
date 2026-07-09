extends StaticBody3D

@export var pantalla_path: NodePath = "../Geometria/Panel_Llegadas_Pantalla"

var mostrando_horario_falso := false

func interact() -> void:
	mostrando_horario_falso = not mostrando_horario_falso
	var pantalla = get_node_or_null(pantalla_path)
	if pantalla and pantalla.get_surface_override_material_count() > 0:
		pass
	print("[Panel de llegadas] ", "Muestra: PROX. TREN 03:14 - VIA 1 (no existe en el horario real)"
		if mostrando_horario_falso else "Pantalla normal")
