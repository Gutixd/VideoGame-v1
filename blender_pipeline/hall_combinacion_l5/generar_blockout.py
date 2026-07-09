"""
LINEA CERO - Hall de Combinacion Baquedano (L1 <-> L5) - Zona 01B
Fase 3.1 - Blockout (solo cajas, sin detalle)

Ejecutar en modo headless:
    blender --background --python generar_blockout.py

Todas las medidas provienen de MAPA_HallCombinacionL5.md seccion 5.
Las marcadas [ESTIMADO] en ese documento NO tienen fuente publica
exacta -- se mantienen etiquetadas como tal en este comentario y en
el documento de diseno, no se presentan como medidas verificadas.

PENDIENTE (condiciones de aprobacion del productor, no resolver aqui):
  - Mural "Agora": no se modela ni texturiza mas alla de un placeholder
    plano hasta conseguir foto real (ver referencias_fotograficas/).
  - Accesos post-renovacion 2024 y escaleras mecanicas reales: la
    geometria actual es [ESTIMADO] por inferencia, se actualizara
    cuando haya fotografia en persona (ver README de referencias).

Convencion de coordenadas (igual que anden_baquedano):
    X_doc = Este / Oeste       -> Blender X
    Y_doc = Altura (up)        -> Blender Z
    Z_doc = Sur / Norte        -> Blender Y

Nota de integracion vertical [ESTIMADO]: el hall se modela con piso
propio en Y_doc=0. La conexion hacia el Anden L1 ya construido queda
al final del segundo tramo de escalera, a Y_doc=-5.0 (caida total
estimada de 5m en 2 tramos). Al integrar ambas escenas en un padre
comun, la instancia de anden_baquedano.tscn debe desplazarse -5.0 en
Y para que su piso (Y=0 local) coincida con este punto de conexion.
Esta cifra es una inferencia de diseno, no una medida real -- ver
seccion 2 y 15 de MAPA_HallCombinacionL5.md.
"""

import bpy
import os

# ---------------------------------------------------------------------------
# Setup (identico a anden_baquedano/generar_blockout.py)
# ---------------------------------------------------------------------------

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)


def crear_coleccion(nombre, padre=None):
    if nombre in bpy.data.collections:
        return bpy.data.collections[nombre]
    col = bpy.data.collections.new(nombre)
    destino = padre if padre else bpy.context.scene.collection
    destino.children.link(col)
    return col


def doc_a_blender_pos(x, y, z):
    return (x, z, y)


def doc_a_blender_size(sx, sy, sz):
    return (sx, sz, sy)


def crear_caja(nombre, coleccion, pos_doc, size_doc):
    bx, by, bz = doc_a_blender_pos(*pos_doc)
    sx, sy, sz = doc_a_blender_size(*size_doc)

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz))
    obj = bpy.context.active_object
    obj.name = nombre
    obj.data.name = nombre + "_Mesh"
    obj.scale = (sx, sy, sz)

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    for col in obj.users_collection:
        col.objects.unlink(obj)
    coleccion.objects.link(obj)
    return obj


# ---------------------------------------------------------------------------
# Construccion del blockout
# ---------------------------------------------------------------------------

def generar():
    limpiar_escena()
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

    col_raiz = crear_coleccion("Hall_Combinacion_L5")
    col_blockout = crear_coleccion("Blockout", padre=col_raiz)

    # --- Hall (20 x 25 x 4.5, todo [ESTIMADO]) -----------------------------
    crear_caja("BLOCK_Piso_Hall", col_blockout,
               pos_doc=(0, 0, 0), size_doc=(20, 0.2, 25))
    crear_caja("BLOCK_Techo_Hall", col_blockout,
               pos_doc=(0, 4.5, 0), size_doc=(20, 0.2, 25))
    crear_caja("BLOCK_Muro_Norte_Hall", col_blockout,
               pos_doc=(0, 2.25, -12.5), size_doc=(20, 4.5, 0.5))
    crear_caja("BLOCK_Muro_Sur_Hall", col_blockout,
               pos_doc=(0, 2.25, 12.5), size_doc=(20, 4.5, 0.5))
    crear_caja("BLOCK_Muro_Este_Hall", col_blockout,
               pos_doc=(10, 2.25, 0), size_doc=(0.5, 4.5, 25))
    crear_caja("BLOCK_Muro_Oeste_Hall", col_blockout,
               pos_doc=(-10, 2.25, 0), size_doc=(0.5, 4.5, 25))

    # --- Torniquetes (5, [ESTIMADO]) ---------------------------------------
    for i, x in enumerate((-6, -3, 0, 3, 6), start=1):
        crear_caja(f"BLOCK_Torniquete_{i:02d}", col_blockout,
                   pos_doc=(x, 0.5, -5), size_doc=(0.4, 1.0, 0.6))

    # --- Servicios (volumenes, [ESTIMADO]) ---------------------------------
    crear_caja("BLOCK_Boleteria", col_blockout,
               pos_doc=(-8, 1.1, -3), size_doc=(2.5, 2.2, 2))
    crear_caja("BLOCK_Bibliometro", col_blockout,
               pos_doc=(7, 1.1, -3), size_doc=(2.5, 2.2, 2))
    crear_caja("BLOCK_Local_Comercial", col_blockout,
               pos_doc=(7, 1.1, 3), size_doc=(2.5, 2.2, 2))

    # --- Escaleras hacia Anden L1 (2 tramos, caida total -5.0m [ESTIMADO]) -
    # NOTA: escaleras mecanicas reales confirmadas en fuentes, pero su
    # geometria/dimension exacta NO -- pendiente de foto en persona.
    crear_caja("BLOCK_Escalera_Tramo1", col_blockout,
               pos_doc=(0, -1.25, 16), size_doc=(4, 2.5, 4))
    crear_caja("BLOCK_Descanso", col_blockout,
               pos_doc=(0, -2.5, 19), size_doc=(4, 0.2, 2))
    crear_caja("BLOCK_Escalera_Tramo2", col_blockout,
               pos_doc=(0, -3.75, 21), size_doc=(4, 2.5, 4))
    crear_caja("BLOCK_Conexion_AndenL1", col_blockout,
               pos_doc=(0, -5.0, 23), size_doc=(4, 0.2, 1))

    # --- Bifurcacion y descenso hacia Anden L5 ([ESTIMADO]) ----------------
    crear_caja("BLOCK_Pasillo_L5", col_blockout,
               pos_doc=(12, 0, 4), size_doc=(4, 4, 8))
    crear_caja("BLOCK_Escalera_L5", col_blockout,
               pos_doc=(12, -5, 10), size_doc=(4, 10, 6))

    # --- Anden L5 (60m, perfil moderno -- ver seccion 0 del doc) -----------
    crear_caja("BLOCK_Piso_AndenL5", col_blockout,
               pos_doc=(12, -10, 20), size_doc=(7, 0.2, 60))
    crear_caja("BLOCK_Techo_AndenL5", col_blockout,
               pos_doc=(12, -6, 20), size_doc=(14, 0.2, 60))
    crear_caja("BLOCK_Muro_Lateral_AndenL5_Oeste", col_blockout,
               pos_doc=(8.25, -8, 20), size_doc=(0.5, 4, 60))
    crear_caja("BLOCK_Muro_Lateral_AndenL5_Este", col_blockout,
               pos_doc=(15.75, -8, 20), size_doc=(0.5, 4, 60))

    # --- Reja de plataforma reservada Linea 7 (dato real confirmado) ------
    crear_caja("BLOCK_Reja_PlataformaL7", col_blockout,
               pos_doc=(12, -8, 48), size_doc=(3.5, 3, 0.1))

    print(f"[LINEA CERO] Blockout Hall+L5 generado: {len(col_blockout.objects)} objetos")


# ---------------------------------------------------------------------------
# Guardado y exportacion
# ---------------------------------------------------------------------------

def guardar_y_exportar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(base_dir, "hall_combinacion_l5_blockout.blend")
    glb_dir = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "models", "hall_combinacion_l5"))
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, "hall_combinacion_l5_blockout.glb")

    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[LINEA CERO] .blend guardado en: {blend_path}")

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_apply=True,
    )
    print(f"[LINEA CERO] .glb exportado en: {glb_path}")


if __name__ == "__main__":
    generar()
    guardar_y_exportar()
