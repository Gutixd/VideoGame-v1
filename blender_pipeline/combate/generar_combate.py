"""
LINEA CERO - Assets de combate: PISTOLA (viewmodel) + ENEMIGO con cuchillo.
Modelado 100% en Blender (bpy), export .glb Y-up para Godot.

Convencion: "adelante" del player/arma es +Y en Blender -> -Z en Godot.
  - Pistola: origen en la culata (comodo para colgar de la camara).
  - Enemigo: origen en la base (pies, Z=0), de pie, mirando +Y (=-Z Godot).

Ejecutar headless:
    blender --background --python generar_combate.py
"""

import bpy
import math
import os


def limpiar():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)
    for mat in list(bpy.data.materials):
        if mat.users == 0:
            bpy.data.materials.remove(mat)


def _set(bsdf, nombres, val):
    for n in nombres:
        if n in bsdf.inputs:
            bsdf.inputs[n].default_value = val
            return


def material(nombre, color, metallic=0.0, roughness=0.6, emis=None, emis_f=0.0):
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    bsdf = None
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            bsdf = n
            break
    if bsdf:
        _set(bsdf, ["Base Color"], (*color, 1.0))
        _set(bsdf, ["Metallic"], metallic)
        _set(bsdf, ["Roughness"], roughness)
        if emis is not None:
            _set(bsdf, ["Emission Color", "Emission"], (*emis, 1.0))
            _set(bsdf, ["Emission Strength"], emis_f)
    return mat


def poner_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


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
# PISTOLA (viewmodel, apunta +Y)
# ---------------------------------------------------------------------------

def construir_pistola():
    mat_metal = material("Pistola_Metal", (0.08, 0.08, 0.09), metallic=0.85, roughness=0.35)
    mat_grip = material("Pistola_Grip", (0.03, 0.03, 0.035), roughness=0.7)

    p = []
    # Corredera / cañon (arriba, a lo largo de +Y)
    p.append(caja("Pist_Corredera", (0.0, 0.09, 0.0), (0.032, 0.20, 0.05), mat=mat_metal))
    # Boca del cañon
    p.append(caja("Pist_Boca", (0.0, 0.20, 0.0), (0.024, 0.02, 0.03), mat=mat_metal))
    # Empuñadura (baja hacia atras y abajo)
    p.append(caja("Pist_Grip", (0.0, -0.02, -0.09), (0.03, 0.05, 0.14), rot=(18, 0, 0), mat=mat_grip))
    # Guardamonte
    p.append(caja("Pist_Guarda", (0.0, 0.02, -0.035), (0.026, 0.05, 0.012), mat=mat_metal))
    # Gatillo
    p.append(caja("Pist_Gatillo", (0.0, 0.015, -0.02), (0.01, 0.012, 0.02), mat=mat_metal))
    return unir(p, "Pistola")


# ---------------------------------------------------------------------------
# ENEMIGO con cuchillo (humanoide blockout, origen en pies Z=0, mira +Y)
# ---------------------------------------------------------------------------

def construir_enemigo():
    mat_ropa = material("Enemigo_Ropa", (0.06, 0.07, 0.09), roughness=0.85)     # ropa oscura (ladron)
    mat_capucha = material("Enemigo_Capucha", (0.04, 0.045, 0.06), roughness=0.9)
    mat_piel = material("Enemigo_Piel", (0.55, 0.4, 0.34), roughness=0.75)
    mat_ojos = material("Enemigo_Ojos", (1, 1, 1), emis=(0.9, 0.95, 1.0), emis_f=5.0)  # ojos brillantes (PH)
    mat_hoja = material("Cuchillo_Hoja", (0.75, 0.78, 0.82), metallic=0.9, roughness=0.25)
    mat_mango = material("Cuchillo_Mango", (0.02, 0.02, 0.02), roughness=0.6)

    p = []
    # Piernas
    p.append(caja("Ene_PiernaL", (-0.11, 0, 0.42), (0.15, 0.16, 0.84), mat=mat_ropa))
    p.append(caja("Ene_PiernaR", (0.11, 0, 0.42), (0.15, 0.16, 0.84), mat=mat_ropa))
    # Torso
    p.append(caja("Ene_Torso", (0.0, 0.0, 1.12), (0.42, 0.24, 0.6), mat=mat_ropa))
    # Cuello
    p.append(caja("Ene_Cuello", (0.0, 0.0, 1.46), (0.12, 0.12, 0.1), mat=mat_piel))
    # Cabeza
    p.append(caja("Ene_Cabeza", (0.0, 0.0, 1.6), (0.23, 0.24, 0.26), mat=mat_piel))
    # Capucha (encima de la cabeza y hombros)
    p.append(caja("Ene_Capucha", (0.0, -0.02, 1.68), (0.28, 0.29, 0.2), mat=mat_capucha))
    # Ojos brillantes (PH) al frente de la cabeza (+Y)
    p.append(caja("Ene_OjoL", (-0.05, 0.12, 1.62), (0.04, 0.02, 0.03), mat=mat_ojos))
    p.append(caja("Ene_OjoR", (0.05, 0.12, 1.62), (0.04, 0.02, 0.03), mat=mat_ojos))
    # Brazo izquierdo (al costado)
    p.append(caja("Ene_BrazoL", (-0.26, 0.0, 1.12), (0.1, 0.1, 0.58), mat=mat_ropa))
    # Brazo derecho extendido al frente (empuñando cuchillo)
    p.append(caja("Ene_BrazoR_hombro", (0.26, 0.06, 1.28), (0.1, 0.1, 0.34), rot=(60, 0, 0), mat=mat_ropa))
    p.append(caja("Ene_BrazoR_ante", (0.26, 0.28, 1.36), (0.09, 0.28, 0.09), mat=mat_ropa))
    p.append(caja("Ene_Mano", (0.26, 0.44, 1.36), (0.1, 0.1, 0.1), mat=mat_piel))
    # Cuchillo en la mano (hoja hacia +Y)
    p.append(caja("Ene_Cuch_Mango", (0.26, 0.5, 1.36), (0.03, 0.1, 0.035), mat=mat_mango))
    p.append(caja("Ene_Cuch_Hoja", (0.26, 0.64, 1.37), (0.015, 0.18, 0.05), mat=mat_hoja))

    return unir(p, "Enemigo_Cuchillo")


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------

def exportar(obj, subcarpeta, nombre_archivo):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    glb_dir = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "models", subcarpeta))
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, nombre_archivo)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB',
                              use_selection=True, export_yup=True, export_apply=True)
    print(f"[LINEA CERO] .glb exportado: {glb_path}")


if __name__ == "__main__":
    limpiar()
    bpy.context.scene.unit_settings.system = 'METRIC'

    pistola = construir_pistola()
    enemigo = construir_enemigo()

    exportar(pistola, "player_viewmodel", "pistola.glb")
    exportar(enemigo, "enemigo", "enemigo_cuchillo.glb")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(base_dir, "combate.blend"))
    print("[LINEA CERO] Pistola + Enemigo generados")
