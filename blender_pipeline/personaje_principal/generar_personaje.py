"""
Genera el personaje principal (protagonista): version detallada, redondeada,
con colores segun la referencia (chaqueta verde-azulada oscura, playera gris,
jeans oscuros, mochila negra con correas, zapatillas con cordon amarillo).

Ejecutar headless:
  blender --background --python generar_personaje.py

Salida:
  blender_pipeline/personaje_principal/personaje.blend (fuente editable)
  assets/models/personaje_principal/personaje.glb (para Godot)
"""
import bpy
import os
import math

# ---------------------------------------------------------------- limpieza
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.meshes):
    bpy.data.meshes.remove(block)
for block in list(bpy.data.materials):
    bpy.data.materials.remove(block)

COL = bpy.data.collections.new("Personaje")
bpy.context.scene.collection.children.link(COL)


def mat(nombre, color, rugosidad=0.6, emision=False, metal=0.0):
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    bsdf = None
    for node in m.node_tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            bsdf = node
            break
    if bsdf is None:
        m.diffuse_color = (*color, 1.0)
        return m
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rugosidad
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = metal
    if emision:
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 1.4
    return m


MAT_CHAQUETA = mat("Chaqueta", (0.055, 0.20, 0.215))
MAT_PLAYERA = mat("Playera", (0.72, 0.72, 0.71), rugosidad=0.8)
MAT_PANTALON = mat("Pantalon", (0.135, 0.12, 0.115))
MAT_PIEL = mat("Piel", (0.80, 0.62, 0.50), rugosidad=0.55)
MAT_PELO = mat("Pelo", (0.10, 0.075, 0.06), rugosidad=0.4)
MAT_OJO = mat("Ojo", (0.05, 0.04, 0.04), rugosidad=0.25)
MAT_ZAPATO = mat("Zapato", (0.09, 0.09, 0.10))
MAT_SUELA = mat("Suela", (0.85, 0.83, 0.78))
MAT_ACENTO = mat("Acento", (0.95, 0.76, 0.05), emision=True)
MAT_MOCHILA = mat("Mochila", (0.11, 0.11, 0.13))
MAT_ZIPPER = mat("Zipper", (0.55, 0.55, 0.58), rugosidad=0.3, metal=0.6)


def _terminar(obj, material, suave=True, bevel=True):
    obj.data.materials.append(material)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    COL.objects.link(obj)
    if bevel:
        bev = obj.modifiers.new("Bevel", "BEVEL")
        bev.width = 0.01
        bev.segments = 3
    if suave:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()
    return obj


def caja(nombre, size, pos, material, rot=(0, 0, 0), bevel=True):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.scale = (size[0], size[1], size[2])
    obj.rotation_euler = tuple(math.radians(a) for a in rot)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return _terminar(obj, material, bevel=bevel)


def cilindro(nombre, radio, alto, pos, material, rot=(0, 0, 0), vertices=10, bevel=True):
    bpy.ops.mesh.primitive_cylinder_add(radius=radio, depth=alto, vertices=vertices, location=pos)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.rotation_euler = tuple(math.radians(a) for a in rot)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    return _terminar(obj, material, bevel=bevel)


def esfera(nombre, radio, pos, material, escala=(1, 1, 1), bevel=False):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radio, location=pos, segments=16, ring_count=10)
    obj = bpy.context.active_object
    obj.name = nombre
    obj.scale = escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _terminar(obj, material, bevel=bevel)


# ------------------------------------------------------------ proporciones
# Origen en los pies (Z=0 hacia arriba). Altura total ~1.78 m.

# --- piernas: muslo + pantorrilla, cilindros (separadas, sin fundirse) ---
for lado, x in [("Izq", -0.125), ("Der", 0.125)]:
    cilindro(f"Muslo_{lado}", 0.072, 0.42, (x, 0, 0.70), MAT_PANTALON)
    cilindro(f"Pantorrilla_{lado}", 0.058, 0.38, (x, 0.006, 0.28), MAT_PANTALON)

# --- zapatillas ---
for lado, x in [("Izq", -0.125), ("Der", 0.125)]:
    caja(f"Zapato_{lado}", (0.10, 0.26, 0.10), (x, 0.03, 0.05), MAT_ZAPATO)
    caja(f"Suela_{lado}", (0.105, 0.27, 0.03), (x, 0.03, 0.005), MAT_SUELA)
    caja(f"Cordon_{lado}", (0.06, 0.02, 0.02), (x, -0.05, 0.095), MAT_ACENTO)

# --- cadera ---
caja("Cadera", (0.27, 0.19, 0.16), (0, 0, 0.955), MAT_PANTALON)

# --- torso (jacket) ---
TORSO_Z = 1.245
caja("Torso", (0.38, 0.21, 0.44), (0, 0, TORSO_Z), MAT_CHAQUETA)
TORSO_TOP = TORSO_Z + 0.22  # 1.465
# playera visible en el cuello (fina, sin bisel para que no se deforme)
caja("Cuello_Playera", (0.10, 0.03, 0.04), (0, -0.095, TORSO_TOP - 0.005), MAT_PLAYERA, bevel=False)
# cierre/zipper al centro
caja("Zipper", (0.018, 0.006, 0.40), (0, -0.106, TORSO_Z), MAT_ZIPPER, bevel=False)

# --- brazos: hombro + antebrazo, pegados al torso, colgando naturalmente ---
SHOULDER_Z = TORSO_TOP - 0.06  # 1.405
for lado, signo in [("Izq", -1), ("Der", 1)]:
    x_hombro = signo * 0.195
    z_brazo = SHOULDER_Z - 0.14
    cilindro(f"Brazo_{lado}", 0.058, 0.28, (x_hombro, 0, z_brazo), MAT_CHAQUETA)
    z_antebrazo = z_brazo - 0.14 - 0.13
    cilindro(f"Antebrazo_{lado}", 0.049, 0.26, (x_hombro, 0, z_antebrazo), MAT_CHAQUETA)
    z_mano = z_antebrazo - 0.13 - 0.05
    esfera(f"Mano_{lado}", 0.048, (x_hombro, 0, z_mano), MAT_PIEL, escala=(0.9, 1.15, 1.0))

# --- cuello y cabeza ---
CUELLO_Z = TORSO_TOP + 0.02
cilindro("Cuello", 0.058, 0.09, (0, 0, CUELLO_Z), MAT_PIEL)
CABEZA_Z = CUELLO_Z + 0.045 + 0.10
esfera("Cabeza", 0.115, (0, 0, CABEZA_Z), MAT_PIEL, escala=(0.92, 1.0, 1.06))

# --- rostro: ojos y boca (chicos, pegados a la cara) ---
for lado, x in [("Izq", -0.042), ("Der", 0.042)]:
    esfera(f"Ojo_{lado}", 0.011, (x, -0.108, CABEZA_Z + 0.01), MAT_OJO, bevel=False)
caja("Boca", (0.045, 0.006, 0.008), (0, -0.113, CABEZA_Z - 0.04), MAT_OJO, bevel=False)

# --- pelo: gorra ajustada + flequillo curvo, sin cubrir la cara ---
esfera("Pelo_Base", 0.121, (0, 0.008, CABEZA_Z + 0.013), MAT_PELO, escala=(0.99, 1.0, 0.92))
esfera("Flequillo", 0.10, (0, -0.05, CABEZA_Z + 0.085), MAT_PELO, escala=(1.05, 0.55, 0.42))

# --- mochila (detras del torso, sin correas visibles por ahora) ---
caja("Mochila", (0.28, 0.14, 0.34), (0, 0.16, TORSO_Z - 0.01), MAT_MOCHILA)

# ---------------------------------------------------------------- guardar
base_dir = os.path.dirname(os.path.abspath(__file__))
blend_path = os.path.join(base_dir, "personaje.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

# --------------------------------------------------------------- exportar
repo_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
out_dir = os.path.join(repo_root, "assets", "models", "personaje_principal")
os.makedirs(out_dir, exist_ok=True)
glb_path = os.path.join(out_dir, "personaje.glb")

bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(
    filepath=glb_path,
    export_format="GLB",
    use_selection=True,
    export_yup=True,
    export_apply=True,
)

print("Personaje detallado exportado a:", glb_path)
