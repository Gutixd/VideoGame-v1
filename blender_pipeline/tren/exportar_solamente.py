import bpy, os
base_dir = os.path.dirname(os.path.abspath(__file__))
blend_path = os.path.join(base_dir, "tren.blend")
bpy.ops.wm.open_mainfile(filepath=blend_path)

repo_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
out_dir = os.path.join(repo_root, "assets", "models", "tren")
glb_path = os.path.join(out_dir, "metro.glb")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format="GLB",
    use_selection=True,
    export_yup=True,
    export_apply=True,
)
print("Exportado (sin regenerar nada) a:", glb_path)
