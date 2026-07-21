"""
LÍNEA CERO - Estación Plaza de Maipú (L5) - Zona 05
Fase Blockout v2 — Habitaciones cerradas

Ejecutar en modo headless:
    blender -b -P generar_blockout.py

Convención de coordenadas:
    X_doc = Este / Oeste       -> Blender X
    Y_doc = Altura (up)        -> Blender Z
    Z_doc = Sur / Norte        -> Blender Y

Niveles:
    Superficie   Y = 0.0
    Mezzanine    Y = -5.0   (5 m bajo tierra)
    Andén        Y = -12.0  (12 m bajo tierra)
"""

import bpy
import os

# ---------------------------------------------------------------------------
# Utilidades base
# ---------------------------------------------------------------------------

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for mat in list(bpy.data.materials):
        if mat.users == 0:
            bpy.data.materials.remove(mat)

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

def crear_material(nombre, color_rgb, roughness=0.5, metallic=0.0):
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*color_rgb, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
    return mat

def asignar_material(obj, material):
    if len(obj.data.materials) == 0:
        obj.data.materials.append(material)
    else:
        obj.data.materials[0] = material

def crear_caja(nombre, coleccion, pos_doc, size_doc, material=None):
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
    if material:
        asignar_material(obj, material)
    return obj

def crear_cilindro(nombre, coleccion, pos_doc, size_doc, material=None):
    bx, by, bz = doc_a_blender_pos(*pos_doc)
    radius = size_doc[0] / 2.0
    depth = size_doc[1]
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=(bx, by, bz))
    obj = bpy.context.active_object
    obj.name = nombre
    obj.data.name = nombre + "_Mesh"
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for col in obj.users_collection:
        col.objects.unlink(obj)
    coleccion.objects.link(obj)
    if material:
        asignar_material(obj, material)
    return obj

# ---------------------------------------------------------------------------
# Función para crear una SALA CERRADA (piso + techo + 4 paredes)
# ---------------------------------------------------------------------------
W = 0.3  # grosor de paneles (paredes, piso, techo)

def crear_sala(prefijo, col, centro, tamaño, mat_piso, mat_muro, mat_techo,
               abrir_n=False, abrir_s=False, abrir_e=False, abrir_w=False,
               sin_piso=False, sin_techo=False):
    """
    Crea una habitación cerrada con paneles delgados.
    centro = (cx, cy, cz) en espacio doc — cy es el centro vertical de la sala.
    tamaño = (ancho_x, alto_y, largo_z).
    abrir_X = True para omitir esa pared (conexión a otro espacio).
    """
    cx, cy, cz = centro
    sx, sy, sz = tamaño

    # Piso
    if not sin_piso:
        crear_caja(f"{prefijo}_Piso", col,
                   (cx, cy - sy/2, cz),
                   (sx, W, sz), mat_piso)

    # Techo
    if not sin_techo:
        crear_caja(f"{prefijo}_Techo", col,
                   (cx, cy + sy/2, cz),
                   (sx, W, sz), mat_techo)

    # Pared Oeste (X negativo)
    if not abrir_w:
        crear_caja(f"{prefijo}_Muro_W", col,
                   (cx - sx/2, cy, cz),
                   (W, sy, sz), mat_muro)

    # Pared Este (X positivo)
    if not abrir_e:
        crear_caja(f"{prefijo}_Muro_E", col,
                   (cx + sx/2, cy, cz),
                   (W, sy, sz), mat_muro)

    # Pared Norte (Z negativo)
    if not abrir_n:
        crear_caja(f"{prefijo}_Muro_N", col,
                   (cx, cy, cz - sz/2),
                   (sx, sy, W), mat_muro)

    # Pared Sur (Z positivo)
    if not abrir_s:
        crear_caja(f"{prefijo}_Muro_S", col,
                   (cx, cy, cz + sz/2),
                   (sx, sy, W), mat_muro)


def crear_corredor(prefijo, col, centro, tamaño, mat_piso, mat_muro, mat_techo,
                   abrir_n=False, abrir_s=False):
    """Corredor orientado en Z (norte-sur). Paredes Este/Oeste siempre cerradas."""
    crear_sala(prefijo, col, centro, tamaño, mat_piso, mat_muro, mat_techo,
               abrir_n=abrir_n, abrir_s=abrir_s, abrir_e=False, abrir_w=False)


def crear_rampa(prefijo, col, inicio_doc, fin_doc, ancho, mat_rampa):
    """
    Crea una rampa (plano inclinado) entre dos puntos.
    inicio_doc = (x, y_inicio, z_inicio)
    fin_doc    = (x, y_fin, z_fin)
    """
    import math
    x = inicio_doc[0]
    y1, z1 = inicio_doc[1], inicio_doc[2]
    y2, z2 = fin_doc[1], fin_doc[2]

    # Centro y longitud
    cy = (y1 + y2) / 2.0
    cz = (z1 + z2) / 2.0
    dy = y2 - y1
    dz = z2 - z1
    longitud = math.sqrt(dy*dy + dz*dz)
    angulo = math.atan2(dy, dz)  # ángulo en plano YZ (doc)

    # Crear caja plana y rotarla
    bx, by, bz = doc_a_blender_pos(x, cy, cz)
    # La rampa es una caja larga y delgada
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(bx, by, bz))
    obj = bpy.context.active_object
    obj.name = prefijo
    obj.data.name = prefijo + "_Mesh"
    obj.scale = (ancho, W, 1.0)  # ancho en X, delgado en Y
    # En Blender: Y_blender = Z_doc, Z_blender = Y_doc
    # Rotamos en el eje X de Blender (que es X_doc)
    obj.scale.y = longitud  # Y_blender = Z_doc direction (length of ramp)
    obj.scale.z = W         # Z_blender = Y_doc (thickness)
    obj.rotation_euler.x = -angulo  # rotar para inclinar

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)
    if mat_rampa:
        asignar_material(obj, mat_rampa)
    return obj


# ---------------------------------------------------------------------------
# GENERAR ESTACIÓN COMPLETA
# ---------------------------------------------------------------------------

def generar():
    limpiar_escena()
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

    col_raiz = crear_coleccion("Estacion_Plaza_Maipu")
    col = crear_coleccion("Blockout", padre=col_raiz)

    # ── Materiales ──────────────────────────────────────────────────────
    mat_hormigon  = crear_material("Mat_Hormigon",  (0.45, 0.45, 0.47), roughness=0.6)
    mat_azulejo   = crear_material("Mat_Azulejo",   (0.65, 0.20, 0.15), roughness=0.3)
    mat_techo     = crear_material("Mat_TechoPanel",(0.12, 0.12, 0.14), roughness=0.4, metallic=0.5)
    mat_piso      = crear_material("Mat_Piso",      (0.70, 0.68, 0.65), roughness=0.3)
    mat_metal     = crear_material("Mat_Metal",     (0.50, 0.50, 0.52), roughness=0.2, metallic=0.8)
    mat_balasto   = crear_material("Mat_Balasto",   (0.35, 0.30, 0.25), roughness=0.9)
    mat_calle     = crear_material("Mat_Calle",     (0.30, 0.30, 0.32), roughness=0.8)
    mat_vigas     = crear_material("Mat_Vigas",     (0.20, 0.20, 0.22), roughness=0.3, metallic=0.4)

    # ====================================================================
    # NIVEL 0: SUPERFICIE  (Y = 0)
    # ====================================================================

    # Calle / Plaza (losa grande como referencia de superficie)
    crear_caja("BLOCK_Plaza_Calle", col,
               (0.0, 0.1, 0.0), (60.0, 0.2, 60.0), mat_calle)

    # ── Vestíbulo de entrada (Y=0, a ras de calle) ──
    # Sala de acceso: 10m ancho × 4m alto × 8m largo
    # Abierta al SUR para conectar con el corredor de descenso
    crear_sala("Vestibulo", col,
               centro=(0.0, -2.0, -10.0), tamaño=(10.0, 4.0, 8.0),
               mat_piso=mat_piso, mat_muro=mat_azulejo, mat_techo=mat_techo,
               abrir_s=True)

    # ── Corredor de descenso al mezzanine ──
    # Corredor largo que baja. Hacemos 3 secciones:
    # Sección 1: Corredor horizontal (Y=-2, Z=-6 a Z=0)
    crear_corredor("Corredor_Acceso", col,
                   centro=(0.0, -2.0, -3.0), tamaño=(6.0, 4.0, 6.0),
                   mat_piso=mat_piso, mat_muro=mat_hormigon, mat_techo=mat_techo,
                   abrir_n=True, abrir_s=True)

    # Sección 2: Escalera de descenso — representada como rampa
    # Va de Y=-2 (Z=0) a Y=-5 (Z=8) — bajando 3m en 8m de recorrido
    crear_rampa("Rampa_Descenso_01", col,
                inicio_doc=(0.0, 0.0, 0.0),
                fin_doc=(0.0, -5.0, 8.0),
                ancho=6.0, mat_rampa=mat_piso)

    # Paredes laterales de la rampa
    crear_caja("Rampa01_Muro_W", col,
               (-3.0, -2.5, 4.0), (W, 5.0, 8.0), mat_hormigon)
    crear_caja("Rampa01_Muro_E", col,
               (3.0, -2.5, 4.0), (W, 5.0, 8.0), mat_hormigon)
    # Techo sobre la rampa
    crear_caja("Rampa01_Techo", col,
               (0.0, 0.5, 4.0), (6.0, W, 8.0), mat_techo)

    # ====================================================================
    # NIVEL -1: MEZZANINE  (Y = -5)
    # ====================================================================

    # ── Hall principal del mezzanine ──
    # Gran sala: 24m ancho × 4.5m alto × 20m largo
    # Centro en Y=-5 + 2.25 = -2.75 (piso en Y=-5, techo en Y=-0.5)
    MEZZ_PISO_Y = -5.0
    MEZZ_ALTO = 4.5
    MEZZ_CY = MEZZ_PISO_Y + MEZZ_ALTO / 2.0  # -2.75

    crear_sala("Mezzanine", col,
               centro=(0.0, MEZZ_CY, 18.0), tamaño=(24.0, MEZZ_ALTO, 20.0),
               mat_piso=mat_piso, mat_muro=mat_azulejo, mat_techo=mat_techo,
               abrir_n=True,  # conecta con corredor de acceso
               abrir_s=True)  # conecta con escaleras al andén

    # ── Muro norte del mezzanine con hueco de pasillo ──
    # Pared norte parcial — lado izquierdo
    crear_caja("Mezz_MuroN_Izq", col,
               (-9.0, MEZZ_CY, 8.0), (6.0, MEZZ_ALTO, W), mat_azulejo)
    # Pared norte parcial — lado derecho
    crear_caja("Mezz_MuroN_Der", col,
               (9.0, MEZZ_CY, 8.0), (6.0, MEZZ_ALTO, W), mat_azulejo)

    # ── Boletería (mostrador) ──
    crear_caja("BLOCK_Boleteria", col,
               (-8.0, MEZZ_PISO_Y + 0.6, 14.0), (4.0, 1.2, 2.0), mat_metal)

    # ── Torniquetes (barrera baja) ──
    crear_caja("BLOCK_Torniquetes", col,
               (0.0, MEZZ_PISO_Y + 0.5, 20.0), (16.0, 1.0, 0.5), mat_metal)

    # ── Bancas ──
    for bx in [-6.0, 6.0]:
        crear_caja(f"BLOCK_Banca_{'W' if bx < 0 else 'E'}", col,
                   (bx, MEZZ_PISO_Y + 0.3, 24.0), (2.0, 0.6, 0.8), mat_metal)

    # ── Vigas decorativas del techo del mezzanine ──
    for vz in [12.0, 18.0, 24.0]:
        crear_caja(f"Mezz_Viga_{int(vz)}", col,
                   (0.0, MEZZ_PISO_Y + MEZZ_ALTO - 0.3, vz),
                   (24.0, 0.6, 0.4), mat_vigas)

    # ====================================================================
    # TRANSICIÓN: ESCALERAS MEZZANINE → ANDÉN
    # ====================================================================

    # ── Corredor pre-escalera ──
    crear_corredor("PreEscalera", col,
                   centro=(0.0, MEZZ_CY, 30.0), tamaño=(8.0, MEZZ_ALTO, 4.0),
                   mat_piso=mat_piso, mat_muro=mat_hormigon, mat_techo=mat_techo,
                   abrir_n=True, abrir_s=True)

    # ── Escalera Tramo 1: Y=-5 → Y=-8.5, Z=32 → Z=38 ──
    crear_rampa("Rampa_Descenso_02", col,
                inicio_doc=(0.0, -5.0, 32.0),
                fin_doc=(0.0, -8.5, 38.0),
                ancho=6.0, mat_rampa=mat_piso)
    crear_caja("Rampa02_Muro_W", col,
               (-3.0, -6.75, 35.0), (W, 5.0, 6.0), mat_hormigon)
    crear_caja("Rampa02_Muro_E", col,
               (3.0, -6.75, 35.0), (W, 5.0, 6.0), mat_hormigon)
    crear_caja("Rampa02_Techo", col,
               (0.0, -4.0, 35.0), (6.0, W, 6.0), mat_techo)

    # ── Descanso intermedio ──
    crear_sala("Descanso", col,
               centro=(0.0, -8.5 + 1.75, 40.0), tamaño=(8.0, 3.5, 4.0),
               mat_piso=mat_piso, mat_muro=mat_hormigon, mat_techo=mat_techo,
               abrir_n=True, abrir_s=True)

    # ── Escalera Tramo 2: Y=-8.5 → Y=-12, Z=42 → Z=48 ──
    crear_rampa("Rampa_Descenso_03", col,
                inicio_doc=(0.0, -8.5, 42.0),
                fin_doc=(0.0, -12.0, 48.0),
                ancho=6.0, mat_rampa=mat_piso)
    crear_caja("Rampa03_Muro_W", col,
               (-3.0, -10.25, 45.0), (W, 5.0, 6.0), mat_hormigon)
    crear_caja("Rampa03_Muro_E", col,
               (3.0, -10.25, 45.0), (W, 5.0, 6.0), mat_hormigon)
    crear_caja("Rampa03_Techo", col,
               (0.0, -7.5, 45.0), (6.0, W, 6.0), mat_techo)

    # ====================================================================
    # NIVEL -2: ANDÉN / PLATAFORMA  (Y = -12)
    # ====================================================================

    ANDEN_PISO_Y = -12.0
    ANDEN_ALTO = 5.0  # techo a Y=-7
    ANDEN_CY = ANDEN_PISO_Y + ANDEN_ALTO / 2.0  # -9.5
    ANDEN_LARGO = 80.0  # 80m de andén
    ANDEN_CZ = 48.0 + ANDEN_LARGO / 2.0  # centro en Z=88

    # Ancho total del túnel: 16m (plataforma central 6m + 2 vías de 3.5m + 2 márgenes)
    TUNEL_ANCHO = 16.0

    # ── Piso de la plataforma central (isla) ──
    crear_caja("Anden_Piso", col,
               (0.0, ANDEN_PISO_Y, ANDEN_CZ),
               (6.0, W, ANDEN_LARGO), mat_piso)

    # ── Foso de vías (más bajo que la plataforma) ──
    FOSO_Y = ANDEN_PISO_Y - 1.0  # 1m por debajo de la plataforma
    # Foso oeste
    crear_caja("Foso_Via_W_Piso", col,
               (-5.0, FOSO_Y, ANDEN_CZ),
               (4.0, W, ANDEN_LARGO), mat_balasto)
    # Foso este
    crear_caja("Foso_Via_E_Piso", col,
               (5.0, FOSO_Y, ANDEN_CZ),
               (4.0, W, ANDEN_LARGO), mat_balasto)

    # Borde del andén (escalón entre plataforma y foso)
    for lado, signo in [("W", -1), ("E", 1)]:
        crear_caja(f"Anden_Borde_{lado}", col,
                   (signo * 3.0, ANDEN_PISO_Y - 0.5, ANDEN_CZ),
                   (W, 1.0, ANDEN_LARGO), mat_hormigon)

    # ── Muros del túnel ──
    crear_caja("Tunel_Muro_W", col,
               (-TUNEL_ANCHO/2, ANDEN_CY, ANDEN_CZ),
               (W, ANDEN_ALTO, ANDEN_LARGO), mat_hormigon)
    crear_caja("Tunel_Muro_E", col,
               (TUNEL_ANCHO/2, ANDEN_CY, ANDEN_CZ),
               (W, ANDEN_ALTO, ANDEN_LARGO), mat_hormigon)

    # ── Techo del túnel ──
    crear_caja("Tunel_Techo", col,
               (0.0, ANDEN_PISO_Y + ANDEN_ALTO, ANDEN_CZ),
               (TUNEL_ANCHO, W, ANDEN_LARGO), mat_techo)

    # ── Pared norte del túnel (con hueco de acceso al centro) ──
    TUNEL_Z_NORTE = ANDEN_CZ - ANDEN_LARGO / 2.0
    crear_caja("Tunel_MuroN_Izq", col,
               (-5.0, ANDEN_CY, TUNEL_Z_NORTE),
               (6.0, ANDEN_ALTO, W), mat_hormigon)
    crear_caja("Tunel_MuroN_Der", col,
               (5.0, ANDEN_CY, TUNEL_Z_NORTE),
               (6.0, ANDEN_ALTO, W), mat_hormigon)

    # ── Pared sur del túnel (cerrada — final de la estación) ──
    TUNEL_Z_SUR = ANDEN_CZ + ANDEN_LARGO / 2.0
    crear_caja("Tunel_Muro_S", col,
               (0.0, ANDEN_CY, TUNEL_Z_SUR),
               (TUNEL_ANCHO, ANDEN_ALTO, W), mat_hormigon)

    # ── Columnas del andén ──
    num_columnas = 8
    for i in range(num_columnas):
        cz = TUNEL_Z_NORTE + 8.0 + i * (ANDEN_LARGO - 16.0) / (num_columnas - 1)
        crear_cilindro(f"Columna_Anden_{i+1:02d}", col,
                       (0.0, ANDEN_CY, cz), (0.6, ANDEN_ALTO, 0.6), mat_vigas)

    # ── Sala de Control (caseta al final sur del andén) ──
    crear_caja("BLOCK_Sala_Control", col,
               (-2.0, ANDEN_PISO_Y + 1.5, TUNEL_Z_SUR - 4.0),
               (3.5, 3.0, 3.5), mat_metal)

    # ── Reja Cola de Maniobras (cerca del extremo norte) ──
    crear_caja("BLOCK_Reja_ColaManiobras", col,
               (0.0, ANDEN_CY, TUNEL_Z_NORTE + 3.0),
               (6.0, ANDEN_ALTO, 0.1), mat_metal)

    # ── Señalización: franjas amarillas en borde del andén ──
    mat_amarillo = crear_material("Mat_Amarillo", (0.9, 0.75, 0.1), roughness=0.3)
    for lado, signo in [("W", -1), ("E", 1)]:
        crear_caja(f"Franja_Seguridad_{lado}", col,
                   (signo * 2.7, ANDEN_PISO_Y + 0.01, ANDEN_CZ),
                   (0.4, 0.02, ANDEN_LARGO), mat_amarillo)

    # ── Rieles (representación simplificada) ──
    mat_riel = crear_material("Mat_Riel", (0.4, 0.4, 0.42), roughness=0.2, metallic=0.9)
    for lado_x in [-5.0, -4.0, 4.0, 5.0]:  # 2 rieles por vía
        for offset in [-0.6, 0.6]:
            rx = lado_x + offset * 0.5
            crear_caja(f"Riel_{('W' if lado_x < 0 else 'E')}_{int(abs(offset*10))}", col,
                       (rx, FOSO_Y + 0.1, ANDEN_CZ),
                       (0.08, 0.15, ANDEN_LARGO), mat_riel)

    print(f"[LÍNEA CERO] Blockout Plaza de Maipú v2 generado: {len(col.objects)} objetos.")


# ---------------------------------------------------------------------------
# Guardar y exportar
# ---------------------------------------------------------------------------

def guardar_y_exportar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(base_dir, "plaza_maipu_blockout.blend")
    glb_dir = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "models", "plaza_maipu"))
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, "plaza_maipu_blockout.glb")

    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[LÍNEA CERO] .blend guardado en: {blend_path}")

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_apply=True,
    )
    print(f"[LÍNEA CERO] .glb exportado en: {glb_path}")


if __name__ == "__main__":
    generar()
    guardar_y_exportar()
