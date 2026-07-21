"""
LINEA CERO - Viewmodel del Player: LINTERNA + MANO IZQUIERDA
Modelado 100% en Blender (bpy), export .glb Y-up para Godot.

Convencion: la linterna apunta a lo largo de +Y en Blender, que al exportar
con export_yup se convierte en -Z en Godot (adelante de la camara). Asi, al
colgar el .glb de la Camera3D con transform identidad, la linterna apunta
hacia donde mira el jugador. El origen del conjunto esta en la culata de la
linterna (Y=0), comodo para posicionar frente a la camara.

Objetos:
  - Linterna  (cuerpo + cabeza + bisel + lente emisiva + boton)
  - Mano_Izq  (palma + 4 dedos + pulgar, agarrando el cuerpo)

Ejecutar headless:
    blender --background --python generar_viewmodel.py
"""

import bpy
import math
import os

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def limpiar():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)
    for mat in list(bpy.data.materials):
        if mat.users == 0:
            bpy.data.materials.remove(mat)


def _set_input(bsdf, nombres, valor):
    for n in nombres:
        if n in bsdf.inputs:
            bsdf.inputs[n].default_value = valor
            return


def material(nombre, color, metallic=0.0, roughness=0.6, emision=None, emis_fuerza=0.0):
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    bsdf = None
    for nodo in mat.node_tree.nodes:
        if nodo.type == 'BSDF_PRINCIPLED':
            bsdf = nodo
            break
    if bsdf is None:
        return mat
    _set_input(bsdf, ["Base Color"], (*color, 1.0))
    _set_input(bsdf, ["Metallic"], metallic)
    _set_input(bsdf, ["Roughness"], roughness)
    if emision is not None:
        _set_input(bsdf, ["Emission Color", "Emission"], (*emision, 1.0))
        _set_input(bsdf, ["Emission Strength"], emis_fuerza)
    return mat


def poner_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def cilindro_Y(nombre, y0, y1, radio, verts=24, mat=None):
    """Cilindro con eje a lo largo de Y (Blender), entre y0 y y1."""
    depth = y1 - y0
    cy = (y0 + y1) / 2.0
    bpy.ops.mesh.primitive_cylinder_add(radius=radio, depth=depth, vertices=verts,
                                        location=(0, cy, 0))
    obj = bpy.context.active_object
    obj.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(rotation=True)
    obj.name = nombre
    if mat:
        poner_mat(obj, mat)
    return obj


def caja(nombre, centro, tam, rot=(0, 0, 0), mat=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=centro)
    obj = bpy.context.active_object
    obj.scale = (tam[0], tam[1], tam[2])
    if rot != (0, 0, 0):
        obj.rotation_euler = (math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]))
    bpy.ops.object.transform_apply(rotation=True, scale=True)
    obj.name = nombre
    if mat:
        poner_mat(obj, mat)
    return obj


def unir(objs, nombre):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = nombre
    return obj


# ---------------------------------------------------------------------------
# Modelado
# ---------------------------------------------------------------------------

def construir_linterna():
    mat_cuerpo = material("Linterna_Cuerpo", (0.05, 0.05, 0.06), metallic=0.3, roughness=0.55)
    mat_metal = material("Linterna_Metal", (0.2, 0.2, 0.22), metallic=0.9, roughness=0.35)
    mat_lente = material("Linterna_Lente", (1.0, 0.95, 0.8), emision=(1.0, 0.93, 0.75), emis_fuerza=6.0)
    mat_boton = material("Linterna_Boton", (0.6, 0.1, 0.08), roughness=0.4)

    partes = []
    # Culata (tapa trasera)
    partes.append(cilindro_Y("Lint_Culata", -0.005, 0.02, 0.026, mat=mat_metal))
    # Cuerpo principal (grip)
    partes.append(cilindro_Y("Lint_Cuerpo", 0.02, 0.17, 0.024, mat=mat_cuerpo))
    # Anillos de agarre (knurl) - dos aros ligeramente mas anchos
    for yc in (0.06, 0.10):
        partes.append(cilindro_Y(f"Lint_Aro_{int(yc*100)}", yc - 0.006, yc + 0.006, 0.026, mat=mat_cuerpo))
    # Cuello hacia la cabeza
    partes.append(cilindro_Y("Lint_Cuello", 0.17, 0.19, 0.03, mat=mat_metal))
    # Cabeza (reflector) - conica: aproximada con cilindro ancho
    partes.append(cilindro_Y("Lint_Cabeza", 0.19, 0.235, 0.042, mat=mat_metal))
    # Bisel frontal
    partes.append(cilindro_Y("Lint_Bisel", 0.235, 0.248, 0.045, mat=mat_metal))
    # Lente emisiva (levemente hundida)
    partes.append(cilindro_Y("Lint_Lente", 0.236, 0.242, 0.04, mat=mat_lente))
    # Boton de encendido (lateral, cerca de la culata)
    partes.append(caja("Lint_Boton", (0.0, 0.035, 0.026), (0.016, 0.022, 0.012), mat=mat_boton))

    linterna = unir(partes, "Linterna")
    return linterna


def construir_mano():
    mat_piel = material("Mano_Piel", (0.62, 0.46, 0.38), roughness=0.75)

    partes = []
    # Palma: bloque bajo el cuerpo de la linterna, envolviendo el grip
    partes.append(caja("Mano_Palma", (0.0, 0.075, -0.032), (0.085, 0.085, 0.05),
                       rot=(8, 0, 0), mat=mat_piel))
    # Nudillos (dorso) sobre el cuerpo
    partes.append(caja("Mano_Dorso", (0.0, 0.085, 0.028), (0.075, 0.06, 0.022),
                       mat=mat_piel))

    # 4 dedos curvandose por encima del cuerpo (lado +Z), en el grip
    xs = (-0.028, -0.009, 0.010, 0.029)
    ys = (0.11, 0.115, 0.112, 0.10)
    for i, (x, y) in enumerate(zip(xs, ys), start=1):
        # falange sobre el tope
        partes.append(caja(f"Mano_Dedo{i}_a", (x, y, 0.03), (0.016, 0.05, 0.018),
                           rot=(55, 0, 0), mat=mat_piel))
        # punta curvada bajando por el frente
        partes.append(caja(f"Mano_Dedo{i}_b", (x, y + 0.018, 0.006), (0.015, 0.03, 0.016),
                           rot=(105, 0, 0), mat=mat_piel))

    # Pulgar sobre el lado (X+), presionando el cuerpo
    partes.append(caja("Mano_Pulgar", (0.03, 0.055, -0.006), (0.018, 0.045, 0.02),
                       rot=(20, 0, -35), mat=mat_piel))

    # Muñeca / antebrazo corto que se pierde fuera de cuadro (hacia -Y, atras)
    partes.append(caja("Mano_Muneca", (0.0, -0.03, -0.05), (0.07, 0.10, 0.06),
                       rot=(15, 0, 0), mat=mat_piel))

    mano = unir(partes, "Mano_Izq")
    return mano


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def guardar_y_exportar(objs):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(base_dir, "viewmodel_player.blend")
    glb_dir = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "models", "player_viewmodel"))
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, "viewmodel_player.glb")

    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[LINEA CERO] .blend guardado: {blend_path}")

    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_apply=True,
    )
    print(f"[LINEA CERO] .glb exportado: {glb_path}")


if __name__ == "__main__":
    limpiar()
    bpy.context.scene.unit_settings.system = 'METRIC'
    linterna = construir_linterna()
    mano = construir_mano()
    print("[LINEA CERO] Viewmodel: Linterna + Mano_Izq generados")
    guardar_y_exportar([linterna, mano])
