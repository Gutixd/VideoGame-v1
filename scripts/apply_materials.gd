@tool
extends EditorScript

const TEX_PATH = "res://assets/textures/"

func _run():
	var mat_hormigon = load(TEX_PATH + "hormigon/Concrete034_1K-JPG.tres")
	var mat_azulejo = load(TEX_PATH + "azulejo_rojo/Tiles141_1K-JPG.tres")
	var mat_terrazo = load(TEX_PATH + "terrazo_piso/Terrazzo013_1K-JPG.tres")
	var mat_metal = load(TEX_PATH + "metal_oxidado/Metal063_1K-JPG.tres")
	var mat_balasto = load(TEX_PATH + "balasto/Gravel023_1K-JPG.tres")
	
	# Enable triplanar for all to fix stretched UVs on the blockout meshes
	for m in [mat_hormigon, mat_azulejo, mat_terrazo, mat_metal, mat_balasto]:
		if m and m is StandardMaterial3D:
			m.uv1_triplanar = true
	
	var scene_root = get_scene()
	if not scene_root or scene_root.name != "EstacionPlazaMaipu":
		print("This script must be run with EstacionPlazaMaipu open in the editor.")
		return
		
	var geometria = scene_root.get_node("Geometria")
	if not geometria:
		print("Geometria node not found!")
		return
		
	var applied_count = 0
	for child in geometria.get_children():
		if child is MeshInstance3D:
			var n = child.name.to_lower()
			var mat = mat_hormigon # Default to concrete
			
			if "piso" in n or "descanso" in n or "plaza" in n:
				mat = mat_terrazo
			elif "muro" in n:
				mat = mat_azulejo
			elif "foso" in n:
				mat = mat_balasto
			elif "techo" in n or "boleteria" in n or "torniquetes" in n or "reja" in n or "sala_control" in n or "viga" in n:
				mat = mat_metal
			
			if mat:
				child.set_surface_override_material(0, mat)
				applied_count += 1
				
	print("Applied PBR materials to ", applied_count, " meshes.")
