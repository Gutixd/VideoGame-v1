import bpy
import math
import os

# Parametros
LARGO_TUNEL = 120.0
ANCHO_TUNEL = 4.5
ALTO_TUNEL = 4.5
SEPARACION_NICHOS = 30.0
RADIO = ANCHO_TUNEL / 2.0

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "assets", "textures"))
GLB_OUT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "assets", "models", "tunel_km14", "tunel_km14.glb"))

# Limpiar escena
bpy.ops.wm.read_factory_settings(use_empty=True)

# Helper para crear colecciones
def get_collection(name):
    if name not in bpy.data.collections:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return bpy.data.collections[name]

# Helper para materiales (usando placeholders simples para el MVP)
def create_material(name, r, g, b):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.9
    return mat

mat_hormigon = create_material("Hormigon", 0.3, 0.3, 0.3)
mat_balasto = create_material("Balasto", 0.1, 0.1, 0.1)
mat_riel = create_material("Riel", 0.5, 0.5, 0.5)
mat_puerta = create_material("PuertaEmergencia", 0.7, 0.2, 0.2)

col_arquitectura = get_collection("Arquitectura")
col_vias = get_collection("Vias")

# 1. Bóveda del túnel (medio cilindro)
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=RADIO, depth=LARGO_TUNEL, location=(0, LARGO_TUNEL/2, 0))
boveda = bpy.context.active_object
boveda.name = "Boveda_Tunel"
boveda.rotation_euler = (math.radians(90), 0, 0)
boveda.data.materials.append(mat_hormigon)
col_arquitectura.objects.link(boveda)
bpy.context.scene.collection.objects.unlink(boveda)

# Eliminar la mitad inferior de la bóveda para hacerla un medio cilindro
bpy.ops.object.select_all(action='DESELECT')
boveda.select_set(True)
bpy.context.view_layer.objects.active = boveda
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.mesh.primitive_cube_add(size=LARGO_TUNEL, location=(0, LARGO_TUNEL/2, -LARGO_TUNEL/2))
cutter = bpy.context.active_object
bool_mod = boveda.modifiers.new(name="CutBottom", type='BOOLEAN')
bool_mod.object = cutter
bool_mod.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = boveda
bpy.ops.object.modifier_apply(modifier="CutBottom")
bpy.data.objects.remove(cutter, do_unlink=True)

# Darle grosor al túnel
solidify = boveda.modifiers.new(name="Solidify", type='SOLIDIFY')
solidify.thickness = 0.2
solidify.offset = 1.0
bpy.ops.object.modifier_apply(modifier="Solidify")

# 2. Piso del túnel (Balasto)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, LARGO_TUNEL/2, -0.1))
piso = bpy.context.active_object
piso.scale = (ANCHO_TUNEL, LARGO_TUNEL, 0.2)
piso.name = "Piso_Balasto"
piso.data.materials.append(mat_balasto)
col_vias.objects.link(piso)
bpy.context.scene.collection.objects.unlink(piso)

# 3. Rieles
for x in [-0.7175, 0.7175]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, LARGO_TUNEL/2, 0.05))
    riel = bpy.context.active_object
    riel.scale = (0.1, LARGO_TUNEL, 0.1)
    riel.name = "Riel" if x < 0 else "Riel.001"
    riel.data.materials.append(mat_riel)
    col_vias.objects.link(riel)
    bpy.context.scene.collection.objects.unlink(riel)

# 4. Nichos de refugio (Booleans en la bóveda)
nichos = []
for i in range(1, int(LARGO_TUNEL / SEPARACION_NICHOS)):
    y_pos = i * SEPARACION_NICHOS
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-RADIO, y_pos, 1.0))
    nicho_cutter = bpy.context.active_object
    nicho_cutter.scale = (1.0, 1.0, 2.0)
    nichos.append(nicho_cutter)
    
    bool_nicho = boveda.modifiers.new(name=f"CutNicho_{i}", type='BOOLEAN')
    bool_nicho.object = nicho_cutter
    bool_nicho.operation = 'DIFFERENCE'

bpy.context.view_layer.objects.active = boveda
for i in range(1, int(LARGO_TUNEL / SEPARACION_NICHOS)):
    bpy.ops.object.modifier_apply(modifier=f"CutNicho_{i}")
    
for cutter in nichos:
    bpy.data.objects.remove(cutter, do_unlink=True)

# 5. Sala de Emergencia (al final del túnel, lado derecho)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(RADIO + 2.5, LARGO_TUNEL - 5.0, 1.5))
sala = bpy.context.active_object
sala.scale = (5.0, 5.0, 3.0)
sala.name = "Sala_Emergencia"
sala.data.materials.append(mat_hormigon)
solidify_sala = sala.modifiers.new(name="Solidify", type='SOLIDIFY')
solidify_sala.thickness = 0.2
solidify_sala.offset = 1.0
bpy.ops.object.modifier_apply(modifier="Solidify")

col_arquitectura.objects.link(sala)
bpy.context.scene.collection.objects.unlink(sala)

# Conectar la sala con el túnel mediante una puerta
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(RADIO, LARGO_TUNEL - 5.0, 1.0))
puerta_cutter = bpy.context.active_object
puerta_cutter.scale = (1.0, 1.5, 2.0)

bool_puerta_tunel = boveda.modifiers.new(name="CutPuerta", type='BOOLEAN')
bool_puerta_tunel.object = puerta_cutter
bool_puerta_tunel.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = boveda
bpy.ops.object.modifier_apply(modifier="CutPuerta")

bool_puerta_sala = sala.modifiers.new(name="CutPuertaSala", type='BOOLEAN')
bool_puerta_sala.object = puerta_cutter
bool_puerta_sala.operation = 'DIFFERENCE'
bpy.context.view_layer.objects.active = sala
bpy.ops.object.modifier_apply(modifier="CutPuertaSala")

bpy.data.objects.remove(puerta_cutter, do_unlink=True)

# 6. Puerta física interactuable
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(RADIO, LARGO_TUNEL - 5.0, 1.0))
puerta_fisica = bpy.context.active_object
puerta_fisica.scale = (0.1, 1.5, 2.0)
puerta_fisica.name = "Puerta_Emergencia"
puerta_fisica.data.materials.append(mat_puerta)
col_arquitectura.objects.link(puerta_fisica)
bpy.context.scene.collection.objects.unlink(puerta_fisica)

# Exportar
os.makedirs(os.path.dirname(GLB_OUT), exist_ok=True)
bpy.ops.export_scene.gltf(
    filepath=GLB_OUT,
    export_format='GLB',
    use_selection=False,
    export_apply=True,
    export_cameras=False,
    export_lights=False
)
print(f"✅ Túnel exportado a {GLB_OUT}")
