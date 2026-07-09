extends Node

# Crea materiales PBR realistas para el metro

static func create_azulejo_rojo() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.8, 0.15, 0.1)  # Rojo Línea 1
	mat.roughness = 0.4
	mat.metallic = 0.0
	mat.normal_scale = 1.0
	return mat

static func create_hormigon() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.65, 0.65, 0.65)  # Gris hormigón
	mat.roughness = 0.8
	mat.metallic = 0.0
	mat.normal_scale = 0.8
	return mat

static func create_metal_oxidado() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.55, 0.45, 0.35)  # Metal oxidado
	mat.roughness = 0.6
	mat.metallic = 0.7
	mat.normal_scale = 0.6
	return mat

static func create_piso_cemento() -> StandardMaterial3D:
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.5, 0.5, 0.52)  # Cemento oscuro
	mat.roughness = 0.9
	mat.metallic = 0.0
	mat.normal_scale = 0.7
	return mat
