"""
LINEA CERO - Anden Baquedano
Fase 3.3 + 3.4 - Estacion completa a escala real (sin comprimir) + Props

Ejecutar en modo headless:
    blender --background --python generar_estacion.py

CAMBIO DE ALCANCE (aprobado explicitamente por el productor):
El documento de diseno original (seccion 15) comprimia el largo real
(~95-110 m estimados) a 55 m jugables por ritmo de gameplay. Esa
decision queda REVERTIDA: esta version construye la estacion a
LARGO_ESTACION = 100 m, dentro del rango real estimado, sin reducir
el ancho (14 m) ni las alturas (4.3 m arranque / 5.5 m clave), que ya
eran reales desde el blockout original.

Todo se genera parametrico a partir de las constantes de la seccion
"PARAMETROS REALES" para que cualquier ajuste futuro de escala no
requiera reescribir posiciones a mano.

Convencion de coordenadas (igual que scripts anteriores):
    X_doc = Este / Oeste       -> Blender X
    Y_doc = Altura (up)        -> Blender Z
    Z_doc = Sur / Norte        -> Blender Y
"""

import bpy
import bmesh
import math
import os

# ---------------------------------------------------------------------------
# PARAMETROS REALES (escala completa, sin comprimir)
# ---------------------------------------------------------------------------

ANCHO_ANDEN = 7.0
ANCHO_VIA = 3.5
ANCHO_TOTAL = ANCHO_ANDEN + 2 * ANCHO_VIA          # 14.0 m
LARGO_ESTACION = 100.0                             # antes 55.0 (comprimido)
ALTURA_ARRANQUE = 4.3
ALZA_BOVEDA = 1.2                                  # clave a 5.5 m
SEPARACION_COLUMNAS = 6.0
ALTURA_ZOCALO = 1.2
ALTURA_FRANJA = ALTURA_ARRANQUE - ALTURA_ZOCALO
GALGA = 0.7175                                     # medio-ancho entre rieles

MEDIO_LARGO = LARGO_ESTACION / 2.0                 # 50.0
MEDIO_ANDEN = ANCHO_ANDEN / 2.0                     # 3.5
X_VIA_OESTE = -(MEDIO_ANDEN + ANCHO_VIA / 2.0)      # -5.25
X_VIA_ESTE = (MEDIO_ANDEN + ANCHO_VIA / 2.0)        # 5.25
X_MURO_LATERAL = ANCHO_TOTAL / 2.0                  # 7.0

MARGEN_COLUMNAS = 2.0
_z = -(MEDIO_LARGO - MARGEN_COLUMNAS)
POSICIONES_COLUMNAS = []
while _z <= (MEDIO_LARGO - MARGEN_COLUMNAS) + 0.01:
    POSICIONES_COLUMNAS.append(round(_z, 2))
    _z += SEPARACION_COLUMNAS

# ---------------------------------------------------------------------------
# Rutas de texturas
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "assets", "textures"))

def tex(carpeta, archivo):
    return os.path.join(TEX_DIR, carpeta, archivo)

RUTAS = {
    "hormigon": {
        "color": tex("hormigon", "Concrete034_1K-JPG_Color.jpg"),
        "normal": tex("hormigon", "Concrete034_1K-JPG_NormalGL.jpg"),
        "rough": tex("hormigon", "Concrete034_1K-JPG_Roughness.jpg"),
    },
    "ceramica": {
        "color": tex("azulejo_rojo", "Tiles141_1K-JPG_Color.jpg"),
        "normal": tex("azulejo_rojo", "Tiles141_1K-JPG_NormalGL.jpg"),
        "rough": tex("azulejo_rojo", "Tiles141_1K-JPG_Roughness.jpg"),
    },
    "metal": {
        "color": tex("metal_oxidado", "Metal063_1K-JPG_Color.jpg"),
        "normal": tex("metal_oxidado", "Metal063_1K-JPG_NormalGL.jpg"),
        "rough": tex("metal_oxidado", "Metal063_1K-JPG_Roughness.jpg"),
    },
    "terrazo": {
        "color": tex("terrazo_piso", "Terrazzo013_1K-JPG_Color.jpg"),
        "normal": tex("terrazo_piso", "Terrazzo013_1K-JPG_NormalGL.jpg"),
        "rough": tex("terrazo_piso", "Terrazzo013_1K-JPG_Roughness.jpg"),
    },
    "balasto": {
        "color": tex("balasto", "Gravel043_1K-JPG_Color.jpg"),
        "normal": tex("balasto", "Gravel043_1K-JPG_NormalGL.jpg"),
        "rough": tex("balasto", "Gravel043_1K-JPG_Roughness.jpg"),
    },
}

_IMG_CACHE = {}

def cargar_imagen(path, non_color=False):
    if path not in _IMG_CACHE:
        img = bpy.data.images.load(path, check_existing=True)
        if non_color:
            img.colorspace_settings.name = 'Non-Color'
        _IMG_CACHE[path] = img
    return _IMG_CACHE[path]


def crear_material_pbr(nombre, set_texturas, tint=None, metallic=0.0,
                        roughness_default=0.5, uv_scale=(1.0, 1.0)):
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    uv_node = nodes.new('ShaderNodeUVMap')
    mapping = nodes.new('ShaderNodeMapping')
    mapping.inputs['Scale'].default_value = (uv_scale[0], uv_scale[1], 1.0)
    links.new(uv_node.outputs['UV'], mapping.inputs['Vector'])

    tex_color = nodes.new('ShaderNodeTexImage')
    tex_color.image = cargar_imagen(set_texturas["color"])
    links.new(mapping.outputs['Vector'], tex_color.inputs['Vector'])

    if tint:
        mix = nodes.new('ShaderNodeMixRGB')
        mix.blend_type = 'MULTIPLY'
        mix.inputs['Fac'].default_value = 1.0
        mix.inputs['Color2'].default_value = (tint[0], tint[1], tint[2], 1.0)
        links.new(tex_color.outputs['Color'], mix.inputs['Color1'])
        links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    else:
        links.new(tex_color.outputs['Color'], bsdf.inputs['Base Color'])

    if set_texturas.get("normal"):
        tex_normal = nodes.new('ShaderNodeTexImage')
        tex_normal.image = cargar_imagen(set_texturas["normal"], non_color=True)
        links.new(mapping.outputs['Vector'], tex_normal.inputs['Vector'])
        normal_map = nodes.new('ShaderNodeNormalMap')
        links.new(tex_normal.outputs['Color'], normal_map.inputs['Color'])
        links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

    if set_texturas.get("rough"):
        tex_rough = nodes.new('ShaderNodeTexImage')
        tex_rough.image = cargar_imagen(set_texturas["rough"], non_color=True)
        links.new(mapping.outputs['Vector'], tex_rough.inputs['Vector'])
        links.new(tex_rough.outputs['Color'], bsdf.inputs['Roughness'])
    else:
        bsdf.inputs['Roughness'].default_value = roughness_default

    bsdf.inputs['Metallic'].default_value = metallic
    return mat


def crear_material_simple(nombre, color, metallic=0.0, roughness=0.5,
                           emission=None, emission_strength=0.0):
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    if emission:
        bsdf.inputs['Emission Color'].default_value = (*emission, 1.0)
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat


# ---------------------------------------------------------------------------
# Utilidades de escena / geometria
# ---------------------------------------------------------------------------

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        if block.users == 0:
            bpy.data.materials.remove(block)


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


def unwrap_basico(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')


def crear_caja(nombre, coleccion, pos_doc, size_doc, material=None, unwrap=True):
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

    if unwrap:
        unwrap_basico(obj)

    if material:
        obj.data.materials.append(material)

    for col in obj.users_collection:
        col.objects.unlink(obj)
    coleccion.objects.link(obj)
    return obj


def crear_cilindro(nombre, coleccion, pos_doc, radio, alto_doc, material=None,
                    vertices=16, rotar_x90=False):
    """Cilindro con eje vertical (Blender Z) salvo rotar_x90=True (eje horizontal Y)."""
    bx, by, bz = doc_a_blender_pos(*pos_doc)
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radio, depth=alto_doc,
                                         location=(bx, by, bz))
    obj = bpy.context.active_object
    obj.name = nombre
    obj.data.name = nombre + "_Mesh"
    if rotar_x90:
        obj.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    unwrap_basico(obj)
    if material:
        obj.data.materials.append(material)
    for col in obj.users_collection:
        col.objects.unlink(obj)
    coleccion.objects.link(obj)
    return obj


def crear_boveda(nombre, coleccion, ancho, largo, altura_arranque, alza, material=None, segmentos=32):
    medio_ancho = ancho / 2.0
    radio = (medio_ancho ** 2 + alza ** 2) / (2 * alza)
    theta_max = math.asin(medio_ancho / radio)
    medio_largo = largo / 2.0

    mesh = bpy.data.meshes.new(nombre + "_Mesh")
    bm = bmesh.new()

    anillo_norte = []
    anillo_sur = []
    for i in range(segmentos + 1):
        t = -theta_max + i * (2 * theta_max) / segmentos
        x = radio * math.sin(t)
        z = altura_arranque + radio * (math.cos(t) - math.cos(theta_max))
        anillo_norte.append(bm.verts.new((x, -medio_largo, z)))
        anillo_sur.append(bm.verts.new((x, medio_largo, z)))

    bm.verts.ensure_lookup_table()
    for i in range(segmentos):
        bm.faces.new((anillo_norte[i], anillo_norte[i + 1],
                       anillo_sur[i + 1], anillo_sur[i]))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(nombre, mesh)
    coleccion.objects.link(obj)

    unwrap_basico(obj)
    if material:
        obj.data.materials.append(material)
        material.use_backface_culling = False
    return obj


# ---------------------------------------------------------------------------
# Props (Fase 3.4)
# ---------------------------------------------------------------------------

def crear_banca(nombre, coleccion, pos_doc, mat_madera, mat_metal):
    contenedor = bpy.data.objects.new(nombre, None)
    coleccion.objects.link(contenedor)
    bx, by, bz = doc_a_blender_pos(*pos_doc)
    contenedor.location = (bx, by, bz)

    asiento = crear_caja(f"{nombre}_Asiento", coleccion,
                          pos_doc=(pos_doc[0], pos_doc[1] + 0.45, pos_doc[2]),
                          size_doc=(1.4, 0.05, 0.45), material=mat_madera)
    respaldo = crear_caja(f"{nombre}_Respaldo", coleccion,
                           pos_doc=(pos_doc[0], pos_doc[1] + 0.75, pos_doc[2] - 0.2),
                           size_doc=(1.4, 0.6, 0.05), material=mat_madera)
    for signo, suf in ((-1, "A"), (1, "B")):
        crear_caja(f"{nombre}_Pata_{suf}", coleccion,
                   pos_doc=(pos_doc[0] + signo * 0.6, pos_doc[1] + 0.22, pos_doc[2]),
                   size_doc=(0.08, 0.45, 0.4), material=mat_metal)
    return contenedor


def crear_basurero(nombre, coleccion, pos_doc, material):
    return crear_cilindro(nombre, coleccion,
                           pos_doc=(pos_doc[0], pos_doc[1] + 0.35, pos_doc[2]),
                           radio=0.22, alto_doc=0.7, material=material, vertices=12)


def crear_extintor(nombre, coleccion, pos_doc, material):
    return crear_cilindro(nombre, coleccion,
                           pos_doc=(pos_doc[0], pos_doc[1] + 0.3, pos_doc[2]),
                           radio=0.09, alto_doc=0.55, material=material, vertices=10)


def crear_caja_herramientas(nombre, coleccion, pos_doc, material):
    return crear_caja(nombre, coleccion, pos_doc=(pos_doc[0], pos_doc[1] + 0.15, pos_doc[2]),
                       size_doc=(0.5, 0.3, 0.3), material=material)


def crear_reloj_anden(nombre, coleccion, pos_doc, mat_carcasa, mat_esfera):
    crear_cilindro(f"{nombre}_Poste", coleccion,
                   pos_doc=(pos_doc[0], pos_doc[1] + 1.0, pos_doc[2]),
                   radio=0.05, alto_doc=2.0, material=mat_carcasa, vertices=8)
    crear_cilindro(f"{nombre}_Esfera", coleccion,
                   pos_doc=(pos_doc[0], pos_doc[1] + 2.1, pos_doc[2]),
                   radio=0.3, alto_doc=0.08, material=mat_esfera, vertices=16,
                   rotar_x90=True)


def crear_cartel_colgante(nombre, coleccion, pos_doc, mat_panel, texto, mat_texto):
    panel = crear_caja(f"{nombre}_Panel", coleccion, pos_doc=pos_doc,
                        size_doc=(2.0, 0.4, 0.06), material=mat_panel)
    bx, by, bz = doc_a_blender_pos(pos_doc[0], pos_doc[1], pos_doc[2] - 0.04)
    bpy.ops.object.text_add(location=(bx, by, bz))
    txt = bpy.context.active_object
    txt.name = f"{nombre}_Texto"
    txt.data.body = texto
    txt.data.size = 0.22
    txt.data.align_x = 'CENTER'
    txt.data.align_y = 'CENTER'
    txt.rotation_euler = (math.radians(90), 0, 0)
    txt.data.materials.append(mat_texto)

    bpy.ops.object.select_all(action='DESELECT')
    txt.select_set(True)
    bpy.context.view_layer.objects.active = txt
    bpy.ops.object.convert(target='MESH')
    txt.data.name = f"{nombre}_Texto_Mesh"

    for col in txt.users_collection:
        col.objects.unlink(txt)
    coleccion.objects.link(txt)
    return panel


# ---------------------------------------------------------------------------
# Construccion de la escena
# ---------------------------------------------------------------------------

def generar():
    limpiar_escena()
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0

    col_raiz = crear_coleccion("Anden_Baquedano")
    col_arquitectura = crear_coleccion("Arquitectura", padre=col_raiz)
    col_senaletica = crear_coleccion("Senaletica", padre=col_raiz)
    col_props = crear_coleccion("Props", padre=col_raiz)

    # --- Materiales ---------------------------------------------------
    mat_hormigon = crear_material_pbr("Hormigon_Boveda", RUTAS["hormigon"],
                                       roughness_default=0.85, uv_scale=(8, 8))
    mat_hormigon_columna = crear_material_pbr("Hormigon_Columna", RUTAS["hormigon"],
                                               tint=(0.75, 0.75, 0.78), roughness_default=0.6,
                                               uv_scale=(1, 2))
    mat_hormigon_muro_cierre = crear_material_pbr("Hormigon_MuroCierre", RUTAS["hormigon"],
                                                   roughness_default=0.85, uv_scale=(3, 2))
    mat_zocalo = crear_material_pbr("Zocalo_Ceramico", RUTAS["ceramica"],
                                     tint=(0.85, 0.8, 0.7), roughness_default=0.3,
                                     uv_scale=(16, 1))
    mat_franja = crear_material_pbr("Franja_Identificadora", RUTAS["ceramica"],
                                     tint=(0.75, 0.55, 0.15), roughness_default=0.35,
                                     uv_scale=(16, 2))
    mat_terrazo = crear_material_pbr("Terrazo_Piso", RUTAS["terrazo"],
                                      roughness_default=0.35, uv_scale=(3, 36))
    mat_balasto = crear_material_pbr("Balasto_Via", RUTAS["balasto"],
                                      roughness_default=0.95, uv_scale=(2, 36))
    mat_riel = crear_material_pbr("Riel_Metalico", RUTAS["metal"],
                                   tint=(0.55, 0.55, 0.58), metallic=0.85,
                                   roughness_default=0.3, uv_scale=(1, 36))
    mat_reja = crear_material_pbr("Reja_Oxidada", RUTAS["metal"],
                                   tint=(0.75, 0.42, 0.22), metallic=0.4,
                                   roughness_default=0.7, uv_scale=(2, 2))
    mat_franja_tactil = crear_material_simple("Franja_Tactil", (0.85, 0.7, 0.05),
                                               metallic=0.0, roughness=0.6)
    mat_panel_carcasa = crear_material_simple("Panel_Carcasa", (0.05, 0.05, 0.06),
                                               metallic=0.3, roughness=0.4)
    mat_panel_pantalla = crear_material_simple("Panel_Pantalla", (0.15, 0.08, 0.0),
                                                emission=(1.0, 0.6, 0.1), emission_strength=2.5)
    mat_madera = crear_material_simple("Madera_Banca", (0.35, 0.22, 0.12), roughness=0.7)
    mat_metal_banca = crear_material_simple("Metal_Banca", (0.2, 0.2, 0.22), metallic=0.6, roughness=0.4)
    mat_basurero = crear_material_simple("Metal_Basurero", (0.25, 0.28, 0.28), metallic=0.5, roughness=0.5)
    mat_extintor = crear_material_simple("Rojo_Extintor", (0.65, 0.05, 0.03), metallic=0.2, roughness=0.4)
    mat_toolbox = crear_material_simple("Caja_Herramientas", (0.55, 0.4, 0.15), metallic=0.3, roughness=0.6)
    mat_reloj_carcasa = crear_material_simple("Reloj_Carcasa", (0.1, 0.1, 0.11), metallic=0.5, roughness=0.4)
    mat_reloj_esfera = crear_material_simple("Reloj_Esfera", (0.9, 0.88, 0.82), roughness=0.3)
    mat_cartel_texto = crear_material_simple("Cartel_Texto", (1.0, 1.0, 1.0),
                                              emission=(1.0, 1.0, 1.0), emission_strength=0.5)

    # --- Piso -----------------------------------------------------------
    crear_caja("Piso_Anden", col_arquitectura,
               pos_doc=(0, 0, 0), size_doc=(ANCHO_ANDEN, 0.2, LARGO_ESTACION), material=mat_terrazo)

    crear_caja("Franja_Tactil_Oeste", col_senaletica,
               pos_doc=(-3.3, 0.01, 0), size_doc=(0.3, 0.02, LARGO_ESTACION), material=mat_franja_tactil)
    crear_caja("Franja_Tactil_Este", col_senaletica,
               pos_doc=(3.3, 0.01, 0), size_doc=(0.3, 0.02, LARGO_ESTACION), material=mat_franja_tactil)

    # --- Muros de cierre ---------------------------------------------------
    crear_caja("Muro_Norte", col_arquitectura,
               pos_doc=(0, 2.15, -MEDIO_LARGO), size_doc=(ANCHO_TOTAL, ALTURA_ARRANQUE, 0.5),
               material=mat_hormigon_muro_cierre)

    crear_caja("Muro_Sur", col_arquitectura,
               pos_doc=(0, 2.15, MEDIO_LARGO), size_doc=(ANCHO_ANDEN, ALTURA_ARRANQUE, 0.5),
               material=mat_hormigon_muro_cierre)

    # --- Muros laterales largos: zocalo + franja identificadora ---------
    for lado, x in (("Oeste", -X_MURO_LATERAL), ("Este", X_MURO_LATERAL)):
        crear_caja(f"Muro_Lateral_{lado}_Zocalo", col_arquitectura,
                   pos_doc=(x, ALTURA_ZOCALO / 2, 0), size_doc=(0.4, ALTURA_ZOCALO, LARGO_ESTACION),
                   material=mat_zocalo)
        crear_caja(f"Muro_Lateral_{lado}_Franja", col_arquitectura,
                   pos_doc=(x, ALTURA_ZOCALO + ALTURA_FRANJA / 2, 0),
                   size_doc=(0.4, ALTURA_FRANJA, LARGO_ESTACION), material=mat_franja)

    # --- Boveda real (arco segmentado) -----------------------------------
    crear_boveda("Boveda", col_arquitectura, ancho=ANCHO_TOTAL, largo=LARGO_ESTACION,
                 altura_arranque=ALTURA_ARRANQUE, alza=ALZA_BOVEDA, material=mat_hormigon)

    # --- Fosos de via (con balasto) ---------------------------------------
    crear_caja("Foso_Via1", col_arquitectura,
               pos_doc=(X_VIA_OESTE, -0.55, 0), size_doc=(ANCHO_VIA, 1.1, LARGO_ESTACION), material=mat_balasto)
    crear_caja("Foso_Via2", col_arquitectura,
               pos_doc=(X_VIA_ESTE, -0.55, 0), size_doc=(ANCHO_VIA, 1.1, LARGO_ESTACION), material=mat_balasto)

    # --- Rieles (2 por via) -------------------------------------------------
    for centro_via, nombre_via in ((X_VIA_OESTE, "Via1"), (X_VIA_ESTE, "Via2")):
        for signo, lado in ((-1, "A"), (1, "B")):
            crear_caja(f"Riel_{nombre_via}_{lado}", col_arquitectura,
                       pos_doc=(centro_via + signo * GALGA, 0.05, 0),
                       size_doc=(0.1, 0.15, LARGO_ESTACION), material=mat_riel)

    # --- Columnas (parametrico, cada 6 m real) ------------------------------
    for i, z in enumerate(POSICIONES_COLUMNAS, start=1):
        crear_caja(f"Columna_{i:02d}", col_arquitectura,
                   pos_doc=(0, 2.15, z), size_doc=(0.6, ALTURA_ARRANQUE, 0.6),
                   material=mat_hormigon_columna)

    # --- Caseta de control -----------------------------------------------
    crear_caja("Caseta_Control", col_arquitectura,
               pos_doc=(1.5, 1.1, 0), size_doc=(2, 2.2, 2), material=mat_zocalo)

    # --- Barreras de seguridad en extremos (relativas al nuevo largo) -----
    for z in (-(MEDIO_LARGO - 1.5), (MEDIO_LARGO - 1.5)):
        etiqueta = "Norte" if z < 0 else "Sur"
        crear_caja(f"Barrera_Oeste_{etiqueta}", col_senaletica,
                   pos_doc=(-3.4, 0.5, z), size_doc=(0.3, 1.0, 0.6), material=mat_reja)
        crear_caja(f"Barrera_Este_{etiqueta}", col_senaletica,
                   pos_doc=(3.4, 0.5, z), size_doc=(0.3, 1.0, 0.6), material=mat_reja)

    # --- Bloqueos ------------------------------------------------------------
    crear_caja("Reja_Escalera_Norte", col_senaletica,
               pos_doc=(0, 1.5, -MEDIO_LARGO + 0.2), size_doc=(3, 3, 0.1), material=mat_reja)

    crear_caja("Reja_Tunel_Este", col_senaletica,
               pos_doc=(X_VIA_ESTE, -0.1, MEDIO_LARGO + 0.1), size_doc=(ANCHO_VIA, 2.0, 0.1),
               material=mat_reja)

    # --- Panel de llegadas (suspendido, cerca del acceso norte) -------------
    crear_caja("Panel_Llegadas_Carcasa", col_senaletica,
               pos_doc=(0, 3.6, -MEDIO_LARGO + 5), size_doc=(2.5, 0.8, 0.2), material=mat_panel_carcasa)
    crear_caja("Panel_Llegadas_Pantalla", col_senaletica,
               pos_doc=(0, 3.6, -MEDIO_LARGO + 5 - 0.11), size_doc=(2.2, 0.5, 0.02),
               material=mat_panel_pantalla)

    # --- Punto de descenso a la via -----------------------------------------
    crear_caja("Descenso_Via", col_arquitectura,
               pos_doc=(-3.75, -0.3, MEDIO_LARGO - 2.5), size_doc=(1.0, 1.1, 2.0), material=mat_terrazo)

    # =====================================================================
    # PROPS (Fase 3.4)
    # =====================================================================

    posiciones_banca = [-30, -6, 18, 36]
    for i, z in enumerate(posiciones_banca, start=1):
        crear_banca(f"Banca_{i:02d}", col_props, pos_doc=(-2.6, 0, z),
                    mat_madera=mat_madera, mat_metal=mat_metal_banca)

    posiciones_basurero = [-18, 6, 30]
    for i, z in enumerate(posiciones_basurero, start=1):
        crear_basurero(f"Basurero_{i:02d}", col_props, pos_doc=(2.8, 0, z), material=mat_basurero)

    for i, z in enumerate((-12, 24), start=1):
        crear_extintor(f"Extintor_{i:02d}", col_props, pos_doc=(0, 0, z), material=mat_extintor)
        # Reposicionar pegado a columna mas cercana en X (junto a muro lateral este)

    crear_caja_herramientas("Caja_Herramientas_Rodrigo", col_props,
                             pos_doc=(-4.2, 0, MEDIO_LARGO - 4), material=mat_toolbox)

    crear_reloj_anden("Reloj_Anden", col_props, pos_doc=(0, 0, -20),
                       mat_carcasa=mat_reloj_carcasa, mat_esfera=mat_reloj_esfera)

    for i, z in enumerate((-40, -2, 40), start=1):
        crear_cartel_colgante(f"Cartel_Baquedano_{i:02d}", col_senaletica,
                                pos_doc=(0, 4.35, z), mat_panel=mat_franja, texto="BAQUEDANO",
                                mat_texto=mat_cartel_texto)

    # Nota de tecnico: panel simple junto a la caseta (contenido narrativo se
    # gestiona via script de gameplay, no geometria)
    crear_caja("Nota_Tecnico", col_props, pos_doc=(2.3, 0.46, 0.6),
               size_doc=(0.25, 0.02, 0.18), material=mat_toolbox)

    total = (len(col_arquitectura.objects) + len(col_senaletica.objects)
             + len(col_props.objects))
    print(f"[LINEA CERO] Estacion completa generada. Objetos totales: {total}. "
          f"Columnas: {len(POSICIONES_COLUMNAS)}. Largo real: {LARGO_ESTACION} m.")


# ---------------------------------------------------------------------------
# Guardado y exportacion
# ---------------------------------------------------------------------------

def guardar_y_exportar():
    blend_path = os.path.join(SCRIPT_DIR, "anden_baquedano_estacion.blend")
    glb_dir = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "assets", "models", "anden_baquedano"))
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, "anden_baquedano_estacion.glb")

    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[LINEA CERO] .blend guardado en: {blend_path}")

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT',
        export_image_format='JPEG',
    )
    print(f"[LINEA CERO] .glb exportado en: {glb_path}")


if __name__ == "__main__":
    generar()
    guardar_y_exportar()
