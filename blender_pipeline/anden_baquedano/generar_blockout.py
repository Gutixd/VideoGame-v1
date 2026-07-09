"""
LINEA CERO - Generador de blockout: Anden Baquedano
Fase 3.1 - Blockout (solo cajas, sin detalle)

Ejecutar en modo headless:
    blender --background --python generar_blockout.py

Convencion de coordenadas del documento de diseno (MAPA_AndenBaquedano.md):
    X_doc = Este (+) / Oeste (-)
    Y_doc = Altura (up)
    Z_doc = Sur (+) / Norte (-)

Blender es Z-up nativo, por lo que se remapea:
    Blender X = X_doc (ancho, Este-Oeste)
    Blender Y = Z_doc (largo, Norte-Sur)
    Blender Z = Y_doc (altura)

El exportador GLTF de Blender (+Y Up) convierte esto automaticamente
a la convencion Y-up que usa Godot, sin necesidad de rotar nada a mano.
"""

import bpy
import os

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)


def crear_coleccion(nombre, padre=None):
    if nombre in bpy.data.collections:
        col = bpy.data.collections[nombre]
    else:
        col = bpy.data.collections.new(nombre)
        destino = padre if padre else bpy.context.scene.collection
        destino.children.link(col)
    return col


def doc_a_blender_pos(x, y, z):
    """Convierte posicion (X_doc=Este, Y_doc=Altura, Z_doc=Sur) a Blender (X,Y,Z)."""
    return (x, z, y)


def doc_a_blender_size(sx, sy, sz):
    """Convierte tamano (ancho, alto, largo) del doc a dimensiones Blender."""
    return (sx, sz, sy)


def crear_caja(nombre, coleccion, pos_doc, size_doc):
    """Crea una caja de blockout con dimensiones reales exactas.

    pos_doc: (x, y, z) centro, convencion del documento de diseno
    size_doc: (ancho_X, alto_Y, largo_Z) dimensiones totales en metros
    """
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

    # Mover de la coleccion Scene Collection a la coleccion destino
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

    col_raiz = crear_coleccion("Anden_Baquedano")
    col_blockout = crear_coleccion("Blockout", padre=col_raiz)

    # --- Piso y cierre del nivel ---------------------------------------
    crear_caja("BLOCK_Piso_Anden", col_blockout,
               pos_doc=(0, 0, 0), size_doc=(7, 0.2, 55))

    crear_caja("BLOCK_Muro_Norte", col_blockout,
               pos_doc=(0, 2.15, -27.5), size_doc=(14, 4.3, 0.5))

    crear_caja("BLOCK_Muro_Sur_Oeste", col_blockout,
               pos_doc=(-3.5, 2.15, 27.5), size_doc=(3.5, 4.3, 0.5))

    crear_caja("BLOCK_Muro_Sur_Este", col_blockout,
               pos_doc=(3.5, 2.15, 27.5), size_doc=(3.5, 4.3, 0.5))

    # --- Boveda (aproximada como caja en blockout puro) -----------------
    # NOTA: el documento original la listaba como cilindro; la regla de
    # blockout exige "solo cajas". La curvatura real se modela en la fase
    # de Materiales/Detalle sobre este mismo volumen de referencia.
    crear_caja("BLOCK_Boveda", col_blockout,
               pos_doc=(0, 4.9, 0), size_doc=(14, 1.2, 55))

    # --- Fosos de via -----------------------------------------------------
    crear_caja("BLOCK_Foso_Via1", col_blockout,
               pos_doc=(-5.25, -0.55, 0), size_doc=(3.5, 1.1, 55))

    crear_caja("BLOCK_Foso_Via2", col_blockout,
               pos_doc=(5.25, -0.55, 0), size_doc=(3.5, 1.1, 55))

    # --- Columnas (9, separacion real de 6 m) ------------------------------
    posiciones_z = [-24, -18, -12, -6, 0, 6, 12, 18, 24]
    for i, z in enumerate(posiciones_z, start=1):
        crear_caja(f"BLOCK_Columna_{i:02d}", col_blockout,
                   pos_doc=(0, 2.15, z), size_doc=(0.6, 4.3, 0.6))

    # --- Caseta de control -------------------------------------------------
    crear_caja("BLOCK_Caseta_Control", col_blockout,
               pos_doc=(1.5, 1.1, 0), size_doc=(2, 2.2, 2))

    # --- Barreras de seguridad en extremos ---------------------------------
    for z in (-26, 26):
        crear_caja(f"BLOCK_Barrera_Oeste_{'Norte' if z < 0 else 'Sur'}",
                   col_blockout, pos_doc=(-3.4, 0.5, z), size_doc=(0.3, 1.0, 0.6))
        crear_caja(f"BLOCK_Barrera_Este_{'Norte' if z < 0 else 'Sur'}",
                   col_blockout, pos_doc=(3.4, 0.5, z), size_doc=(0.3, 1.0, 0.6))

    # --- Bloqueos (rejas) --------------------------------------------------
    crear_caja("BLOCK_Reja_Escalera_Norte", col_blockout,
               pos_doc=(0, 1.5, -27.3), size_doc=(3, 3, 0.1))

    crear_caja("BLOCK_Reja_Tunel_Este", col_blockout,
               pos_doc=(3.5, 2.15, 27.3), size_doc=(3.5, 4, 0.1))

    # --- Panel de llegadas (suspendido) -------------------------------------
    crear_caja("BLOCK_Panel_Llegadas", col_blockout,
               pos_doc=(0, 3.6, -3), size_doc=(2.5, 0.8, 0.2))

    # --- Punto de descenso a la via -----------------------------------------
    crear_caja("BLOCK_Descenso_Via", col_blockout,
               pos_doc=(-2, -0.3, 26), size_doc=(2, 1.1, 1.5))

    print(f"[LINEA CERO] Blockout generado: {len(col_blockout.objects)} objetos")


# ---------------------------------------------------------------------------
# Guardado y exportacion
# ---------------------------------------------------------------------------

def guardar_y_exportar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(base_dir, "anden_baquedano_blockout.blend")
    glb_dir = os.path.join(base_dir, "..", "..", "assets", "models", "anden_baquedano")
    glb_dir = os.path.normpath(glb_dir)
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, "anden_baquedano_blockout.glb")

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
