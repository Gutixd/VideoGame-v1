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
import math

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


def crear_rampa(nombre, coleccion, top_doc, bottom_doc, ancho, espesor=0.4):
    """Rampa inclinada continua (superficie caminable) entre dos puntos.

    top_doc / bottom_doc: puntos (x, y, z) en coordenadas de documento que
    definen la LINEA DE SUPERFICIE de la rampa (donde camina el jugador).
    La caja se inclina rotando alrededor del eje X (Este-Oeste) y se baja
    medio espesor a lo largo de su normal para que la cara superior quede
    exactamente sobre la linea top->bottom (sin escalon/labio en las uniones).

    A diferencia de los "escalones" de cajas planas de la v1 (que dejaban
    caidas verticales de 2.4m y huecos por donde el jugador caia al vacio),
    una rampa es una superficie continua: fisica suave para bajar Y subir,
    consistente con escaleras mecanicas/fijas reales de metro.
    """
    tb = doc_a_blender_pos(*top_doc)      # (bx, by, bz) del punto alto
    bb = doc_a_blender_pos(*bottom_doc)   # del punto bajo
    cx = (tb[0] + bb[0]) / 2.0
    cy = (tb[1] + bb[1]) / 2.0
    cz = (tb[2] + bb[2]) / 2.0

    # Direccion en Blender (esta en el plano Y-Z, x=0 porque ambos comparten X)
    dy = bb[1] - tb[1]
    dz = bb[2] - tb[2]
    largo = math.sqrt(dy * dy + dz * dz)
    ang = math.atan2(dz, dy)   # rotacion alrededor de Blender X

    # Normal "hacia arriba" de la superficie (perpendicular a la direccion,
    # en el plano Y-Z): rotar la direccion +90deg. Bajamos el centro medio
    # espesor por esta normal para que la cara superior toque la linea.
    nz = math.cos(ang)     # componente Z de la normal-arriba
    ny = -math.sin(ang)    # componente Y de la normal-arriba
    cy -= (espesor / 2.0) * ny
    cz -= (espesor / 2.0) * nz

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, cz))
    obj = bpy.context.active_object
    obj.name = nombre
    obj.data.name = nombre + "_Mesh"
    obj.scale = (ancho, largo, espesor)
    obj.rotation_euler = (ang, 0.0, 0.0)

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

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

    # --- Hall (34 x 25 x 4.5, todo [ESTIMADO]) -----------------------------
    # AMPLIADO respecto a la v1: se necesita alcanzar X=14 (segunda
    # escalera hacia Anden_B) y X=20 (rama L5) sin que se superpongan.
    # Centro desplazado a X=7 (antes X=0); el ala oeste (servicios,
    # torniquetes) no cambia de posicion absoluta.
    crear_caja("BLOCK_Piso_Hall", col_blockout,
               pos_doc=(7, 0, 0), size_doc=(34, 0.2, 25))
    crear_caja("BLOCK_Techo_Hall", col_blockout,
               pos_doc=(7, 4.5, 0), size_doc=(34, 0.2, 25))
    # Muro norte en dos piezas, con hueco en X=-6 para la conexion con
    # Sala Tecnica (acceso de mantenimiento, elemento 01 de la seccion 3
    # del doc). Hueco de 4m: de X=-8 a X=-4.
    crear_caja("BLOCK_Muro_Norte_Hall_Oeste", col_blockout,
               pos_doc=(-9, 2.25, -12.5), size_doc=(2, 4.5, 0.5))
    crear_caja("BLOCK_Muro_Norte_Hall_Este", col_blockout,
               pos_doc=(10, 2.25, -12.5), size_doc=(28, 4.5, 0.5))
    # Muro sur en 4 piezas, con 3 vanos reales (antes era una sola losa
    # solida de 34m sin colision asignada en Godot -- nunca bloqueaba ni
    # dejaba pasar correctamente). Vanos de 4m en X=0 (escalera Anden_A),
    # X=14 (escalera Anden_B) y X=20 (pasillo Linea 5).
    crear_caja("BLOCK_Muro_Sur_Hall_A", col_blockout,
               pos_doc=(-6, 2.25, 12.5), size_doc=(8, 4.5, 0.5))
    crear_caja("BLOCK_Muro_Sur_Hall_B", col_blockout,
               pos_doc=(7, 2.25, 12.5), size_doc=(10, 4.5, 0.5))
    crear_caja("BLOCK_Muro_Sur_Hall_C", col_blockout,
               pos_doc=(17, 2.25, 12.5), size_doc=(2, 4.5, 0.5))
    crear_caja("BLOCK_Muro_Sur_Hall_D", col_blockout,
               pos_doc=(23, 2.25, 12.5), size_doc=(2, 4.5, 0.5))
    crear_caja("BLOCK_Muro_Este_Hall", col_blockout,
               pos_doc=(24, 2.25, 0), size_doc=(0.5, 4.5, 25))
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

    # --- Escalera hacia Anden_A / L1 -- RAMPA CONTINUA ---------------------
    # CORRECCION v2 (rework de circulacion): la v1 usaba cajas planas
    # apiladas (Tramo1/Descanso/Tramo2/Conexion) que en realidad NO eran
    # rampas: dejaban caidas verticales de ~2.4m entre cada escalon y, peor,
    # un HUECO de 1.5m entre el borde del piso del Hall (Z=12.5) y el primer
    # escalon (Z=14). Como el Anden L1 esta desplazado al sur (empieza en
    # Z=23 mundo), bajo ese hueco no hay piso: el jugador caia al vacio
    # (Y=-875 observado). Se reemplaza por una rampa inclinada continua del
    # borde del Hall (Y=0.1, Z=12.5) al inicio del anden (Y=-4.9, Z=22.5),
    # ~26.6 grados, caminable de bajada y de subida sin fisica brusca. El
    # descanso final plano solapa el piso del anden para garantizar union.
    crear_rampa("BLOCK_Rampa_AndenA", col_blockout,
                top_doc=(0, 0.1, 12.5), bottom_doc=(0, -4.9, 22.5), ancho=4)
    crear_caja("BLOCK_Conexion_AndenA", col_blockout,
               pos_doc=(0, -5.05, 23), size_doc=(4, 0.3, 2))

    # --- Escalera hacia Anden_B -- RAMPA CONTINUA (sentido opuesto) --------
    # Mismo rework. Alineada con el centro real de Anden_B (X=14).
    crear_rampa("BLOCK_Rampa_AndenB", col_blockout,
                top_doc=(14, 0.1, 12.5), bottom_doc=(14, -4.9, 22.5), ancho=4)
    crear_caja("BLOCK_Conexion_AndenB", col_blockout,
               pos_doc=(14, -5.05, 23), size_doc=(4, 0.3, 2))

    # --- Bifurcacion y descenso hacia Anden L5 ([ESTIMADO]) ----------------
    # CORRECCION: en la v1, Pasillo_L5 y Escalera_L5 se modelaron como
    # cajas SOLIDAS (volumenes de bloqueo, no arquitectura hueca). Al
    # verificar caminando (ver seccion 19.x del MAPA_AndenBaquedano.md)
    # se confirmo que esto dejaba la rama L5 completamente inaccesible:
    # el jugador chocaba contra la cara norte de Pasillo_L5 sin poder
    # entrar. Se reconstruye como piso+muros+techo real, igual que el
    # resto de la estacion, y la escalera pasa a 4 tramos de 2.5m (igual
    # patron que la escalera hacia Anden_A/B) para cubrir el desnivel de
    # 10m con una pendiente caminable.

    # Pasillo L5 (hueco): X=20, Z=0 a 8, nivel del Hall (Y=0)
    crear_caja("BLOCK_Pasillo_L5_Piso", col_blockout,
               pos_doc=(20, -0.1, 4), size_doc=(4, 0.2, 8))
    crear_caja("BLOCK_Pasillo_L5_Techo", col_blockout,
               pos_doc=(20, 3.9, 4), size_doc=(4, 0.2, 8))
    crear_caja("BLOCK_Pasillo_L5_Muro_Oeste", col_blockout,
               pos_doc=(18, 2, 4), size_doc=(0.2, 4, 8))
    crear_caja("BLOCK_Pasillo_L5_Muro_Este", col_blockout,
               pos_doc=(22, 2, 4), size_doc=(0.2, 4, 8))

    # Escalera L5 -- 2 RAMPAS continuas + descanso intermedio (rework).
    # Antes eran 4 cajas planas apiladas (mismo defecto que Anden_A/B:
    # caidas verticales de 2.4m escalon a escalon). El descenso real de
    # una estacion profunda (L5, tuneladora 1997) se hace con tramos de
    # escalera mecanica larga con descanso; se modela como 2 rampas de 5m
    # de caida cada una con un descanso plano intermedio a Y=-5.
    crear_rampa("BLOCK_Rampa_L5_1", col_blockout,
                top_doc=(20, 0.0, 8), bottom_doc=(20, -5.0, 18), ancho=4)
    crear_caja("BLOCK_Descanso_L5", col_blockout,
               pos_doc=(20, -5.15, 19), size_doc=(4, 0.3, 2))
    crear_rampa("BLOCK_Rampa_L5_2", col_blockout,
                top_doc=(20, -5.0, 20), bottom_doc=(20, -9.9, 30), ancho=4)
    crear_caja("BLOCK_Conexion_AndenL5", col_blockout,
               pos_doc=(20, -10.05, 30.5), size_doc=(4, 0.3, 2))

    # --- Anden L5 (60m, perfil moderno -- ver seccion 0 del doc) -----------
    # Reubicado de Z=20 (centro) a Z=60 (centro), es decir Z=30 a Z=90,
    # para dejar espacio a los 4 tramos de escalera (antes terminaba en
    # Z=13 con un desnivel de 10m imposible de caminar en solo 6m).
    crear_caja("BLOCK_Piso_AndenL5", col_blockout,
               pos_doc=(20, -10, 60), size_doc=(7, 0.2, 60))
    crear_caja("BLOCK_Techo_AndenL5", col_blockout,
               pos_doc=(20, -6, 60), size_doc=(14, 0.2, 60))
    crear_caja("BLOCK_Muro_Lateral_AndenL5_Oeste", col_blockout,
               pos_doc=(16.25, -8, 60), size_doc=(0.5, 4, 60))
    crear_caja("BLOCK_Muro_Lateral_AndenL5_Este", col_blockout,
               pos_doc=(23.75, -8, 60), size_doc=(0.5, 4, 60))

    # --- Reja de plataforma reservada Linea 7 (dato real confirmado) ------
    # Ancho ampliado a 7m (todo el andén) para que bloquee de verdad el
    # paso -- antes (3.5m) dejaba espacio libre a los costados y el
    # jugador podia caer al vacio mas alla del piso modelado.
    crear_caja("BLOCK_Reja_PlataformaL7", col_blockout,
               pos_doc=(20, -8, 88), size_doc=(7, 3, 0.3))

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
