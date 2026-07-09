"""
LINEA CERO - Anden Baquedano
Fase 3.3 + 3.4 - Estacion completa a escala real (sin comprimir) + Props
v2: Reconstruccion de materiales/geometria segun fotos reales de referencia

Ejecutar en modo headless:
    blender --background --python generar_estacion.py

CAMBIO DE ALCANCE (aprobado explicitamente por el productor):
El documento de diseno original (seccion 15) comprimia el largo real
(~95-110 m estimados) a 55 m jugables por ritmo de gameplay. Esa
decision quedo REVERTIDA: esta version construye la estacion a
LARGO_ESTACION = 100 m, dentro del rango real estimado, sin reducir
el ancho (14 m).

CORRECCION v2 (fotos reales de referencia aportadas por el productor):
La v1 asumia una boveda de hormigon visto lisa + muros ceramicos
crema/ocre, extrapolado por analogia sin foto real del anden. Fotos
reales muestran:
  - Techo de VIGAS TRANSVERSALES (no boveda lisa), con luces lineales
    montadas bajo cada viga
  - Muros de ceramica color terracota/ladrillo uniforme (no crema+ocre
    en dos tonos)
  - Piso con patron de "manchas" oscuras irregulares sobre base clara
    (aproximado aqui con textura procedural Voronoi, no hay foto en
    angulo perpendicular todavia para convertir a textura real)
  - Columnas CILINDRICAS (no rectangulares)
  - Franja de luz naranja a lo largo de la via (indicador real)
Ver referencias_fotograficas/ para las fotos que motivaron este cambio.

CORRECCION v3 (topologia de anden -- foto real de tren + andenes):
La v1/v2 modelaban un ANDEN UNICO CENTRAL con una via a cada lado
(isla). Una foto real muestra claramente lo contrario: DOS ANDENES
LATERALES separados, cada uno sirviendo un sentido opuesto, con
AMBAS VIAS juntas en el medio (sin plataforma entre ellas). Para
cambiar de sentido los pasajeros suben por una escalera distinta
para cada anden (no hay cruce a nivel de piso).

Se mantiene Anden_A exactamente en su posicion original (X centrado
en 0) para NO romper la conexion ya construida con el Hall (la
escalera del Hall llega a Anden_A sin cambios). Las vias y el
segundo anden (Anden_B) se agregan hacia el Este (X positivo).
Anden_B es explorable pero no es parte del camino critico del
jugador en esta v1 del nivel -- ver seccion de gameplay.

Convencion de coordenadas (igual que scripts anteriores):
    X_doc = Este / Oeste       -> Blender X
    Y_doc = Altura (up)        -> Blender Z
    Z_doc = Sur / Norte        -> Blender Y
"""

import bpy
import math
import os

# ---------------------------------------------------------------------------
# PARAMETROS REALES (escala completa, sin comprimir)
# ---------------------------------------------------------------------------

ANCHO_ANDEN = 7.0
ANCHO_VIA = 3.5
LARGO_ESTACION = 100.0
ALTURA_ARRANQUE = 4.3
ALTURA_TECHO = 5.0                                 # techo de vigas, mas bajo que la boveda v1
SEPARACION_COLUMNAS = 6.0
SEPARACION_VIGAS = 4.0
GALGA = 0.7175

MEDIO_LARGO = LARGO_ESTACION / 2.0
MEDIO_ANDEN = ANCHO_ANDEN / 2.0

# --- Topologia v3: dos andenes laterales, vias juntas en el medio ------
# Anden_A se mantiene centrado en X=0 (posicion original) para no romper
# la conexion ya construida con el Hall. Vias y Anden_B se agregan al Este.
X_ANDEN_A_CENTRO = 0.0
X_MURO_OESTE_ANDEN_A = X_ANDEN_A_CENTRO - MEDIO_ANDEN              # -3.5

X_VIA1_INICIO = X_ANDEN_A_CENTRO + MEDIO_ANDEN                     # 3.5
X_VIA1_CENTRO = X_VIA1_INICIO + ANCHO_VIA / 2.0                    # 5.25
X_VIA2_INICIO = X_VIA1_INICIO + ANCHO_VIA                          # 7.0
X_VIA2_CENTRO = X_VIA2_INICIO + ANCHO_VIA / 2.0                    # 8.75
X_ANDEN_B_INICIO = X_VIA2_INICIO + ANCHO_VIA                       # 10.5
X_ANDEN_B_CENTRO = X_ANDEN_B_INICIO + MEDIO_ANDEN                  # 14.0
X_MURO_ESTE_ANDEN_B = X_ANDEN_B_INICIO + ANCHO_ANDEN               # 17.5

ANCHO_TOTAL = X_MURO_ESTE_ANDEN_B - X_MURO_OESTE_ANDEN_A           # 21.0 m

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


def crear_material_manchas(nombre, color_base, color_manchas, roughness_default=0.3,
                            escala=6.0, umbral=0.35):
    """Patron de 'nubes'/manchas oscuras sobre base clara, via Voronoi procedural.

    Aproximacion deliberada: no existe (todavia) una foto perpendicular
    real del piso para convertir a textura tileable. Ver
    referencias_fotograficas/10_Texturas -- pendiente de reemplazo.
    """
    mat = bpy.data.materials.new(nombre)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])

    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.voronoi_dimensions = '2D'
    voronoi.feature = 'F1'
    voronoi.inputs['Scale'].default_value = escala
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])

    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (*color_manchas, 1.0)
    ramp.color_ramp.elements[1].position = umbral
    ramp.color_ramp.elements[1].color = (*color_base, 1.0)
    links.new(voronoi.outputs['Distance'], ramp.inputs['Fac'])

    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = roughness_default
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


def crear_techo_vigas(coleccion, ancho, largo, altura, separacion, mat_viga, mat_luz, mat_panel):
    """Techo de vigas transversales con luces lineales, segun fotos reales
    (reemplaza la boveda lisa de la v1, que era una suposicion sin foto)."""
    medio_largo = largo / 2.0
    z = -medio_largo + separacion / 2.0
    i = 0
    while z < medio_largo:
        crear_caja(f"Viga_{i:02d}", coleccion, pos_doc=(0, altura, z),
                   size_doc=(ancho, 0.3, 0.4), material=mat_viga)
        crear_caja(f"LuzViga_{i:02d}", coleccion, pos_doc=(0, altura - 0.22, z),
                   size_doc=(ancho * 0.85, 0.05, 0.08), material=mat_luz)
        z += separacion
        i += 1

    crear_caja("Techo_Panel", coleccion, pos_doc=(0, altura + 0.35, 0),
               size_doc=(ancho, 0.1, largo), material=mat_panel)


# ---------------------------------------------------------------------------
# Props (Fase 3.4)
# ---------------------------------------------------------------------------

def crear_banca(nombre, coleccion, pos_doc, mat_madera, mat_metal):
    crear_caja(f"{nombre}_Asiento", coleccion,
               pos_doc=(pos_doc[0], pos_doc[1] + 0.45, pos_doc[2]),
               size_doc=(1.4, 0.05, 0.45), material=mat_madera)
    crear_caja(f"{nombre}_Respaldo", coleccion,
               pos_doc=(pos_doc[0], pos_doc[1] + 0.75, pos_doc[2] - 0.2),
               size_doc=(1.4, 0.6, 0.05), material=mat_madera)
    for signo, suf in ((-1, "A"), (1, "B")):
        crear_caja(f"{nombre}_Pata_{suf}", coleccion,
                   pos_doc=(pos_doc[0] + signo * 0.6, pos_doc[1] + 0.22, pos_doc[2]),
                   size_doc=(0.08, 0.45, 0.4), material=mat_metal)


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
    mat_viga = crear_material_pbr("Hormigon_Viga", RUTAS["hormigon"],
                                   tint=(0.55, 0.53, 0.5), roughness_default=0.7,
                                   uv_scale=(2, 1))
    mat_techo_panel = crear_material_pbr("Panel_Techo", RUTAS["hormigon"],
                                          tint=(0.4, 0.4, 0.42), roughness_default=0.6,
                                          uv_scale=(8, 8))
    mat_luz_viga = crear_material_simple("Luz_Viga_Emisiva", (0.9, 0.9, 0.85),
                                          emission=(1.0, 0.97, 0.85), emission_strength=4.0)
    mat_hormigon_muro_cierre = crear_material_pbr("Hormigon_MuroCierre", RUTAS["hormigon"],
                                                   roughness_default=0.85, uv_scale=(3, 2))
    # Muro de ladrillo/terracota (corregido segun foto real -- ver docstring del modulo)
    mat_muro_ladrillo = crear_material_pbr("Muro_Ladrillo_Terracota", RUTAS["ceramica"],
                                            tint=(0.55, 0.27, 0.18), roughness_default=0.4,
                                            uv_scale=(16, 2))
    mat_columna_ladrillo = crear_material_pbr("Columna_Ladrillo", RUTAS["ceramica"],
                                               tint=(0.5, 0.24, 0.16), roughness_default=0.45,
                                               uv_scale=(2, 3))
    # Piso con patron de manchas (procedural, pendiente de foto real perpendicular)
    mat_piso_manchas = crear_material_manchas("Piso_Manchas", color_base=(0.75, 0.71, 0.62),
                                               color_manchas=(0.28, 0.24, 0.2),
                                               roughness_default=0.65, escala=8.0, umbral=0.45)
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
    mat_franja_via_naranja = crear_material_simple("Franja_Via_Naranja", (0.4, 0.15, 0.02),
                                                    emission=(1.0, 0.45, 0.05), emission_strength=3.0)
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

    # --- Piso: Anden_A (posicion original, sin cambios) + Anden_B (nuevo) ---
    crear_caja("Piso_Anden_A", col_arquitectura,
               pos_doc=(X_ANDEN_A_CENTRO, 0, 0), size_doc=(ANCHO_ANDEN, 0.2, LARGO_ESTACION),
               material=mat_piso_manchas)
    crear_caja("Piso_Anden_B", col_arquitectura,
               pos_doc=(X_ANDEN_B_CENTRO, 0, 0), size_doc=(ANCHO_ANDEN, 0.2, LARGO_ESTACION),
               material=mat_piso_manchas)

    # Franja tactil: cada anden solo tiene un borde (el que da a su via)
    crear_caja("Franja_Tactil_AndenA", col_senaletica,
               pos_doc=(X_VIA1_INICIO - 0.2, 0.01, 0), size_doc=(0.3, 0.02, LARGO_ESTACION),
               material=mat_franja_tactil)
    crear_caja("Franja_Tactil_AndenB", col_senaletica,
               pos_doc=(X_ANDEN_B_INICIO + 0.2, 0.01, 0), size_doc=(0.3, 0.02, LARGO_ESTACION),
               material=mat_franja_tactil)

    # --- Muros de cierre -----------------------------------------------------
    # CORREGIDO: el muro norte completo (21m) bloqueaba fisicamente la
    # conexion con el Hall aunque las coordenadas coincidieran matematicamente
    # -- se verifico caminando (simulacion de input real) que el jugador
    # quedaba atascado contra este muro sin poder entrar. Ahora solo se
    # sella el tramo de las vias (donde el jugador no debe pasar); ambos
    # andenes quedan con su extremo norte abierto hacia el Hall.
    ancho_vias_norte = X_ANDEN_B_INICIO - X_VIA1_INICIO
    centro_vias_norte = (X_VIA1_INICIO + X_ANDEN_B_INICIO) / 2.0
    crear_caja("Muro_Norte_Vias", col_arquitectura,
               pos_doc=(centro_vias_norte, 2.15, -MEDIO_LARGO),
               size_doc=(ancho_vias_norte, ALTURA_ARRANQUE, 0.5), material=mat_hormigon_muro_cierre)

    # Muro sur: cierra cada anden por separado, dejando abierto el tramo de
    # las vias (Via1 transitable hacia el tunel, Via2 sellada con reja)
    crear_caja("Muro_Sur_AndenA", col_arquitectura,
               pos_doc=(X_ANDEN_A_CENTRO, 2.15, MEDIO_LARGO), size_doc=(ANCHO_ANDEN, ALTURA_ARRANQUE, 0.5),
               material=mat_hormigon_muro_cierre)
    crear_caja("Muro_Sur_AndenB", col_arquitectura,
               pos_doc=(X_ANDEN_B_CENTRO, 2.15, MEDIO_LARGO), size_doc=(ANCHO_ANDEN, ALTURA_ARRANQUE, 0.5),
               material=mat_hormigon_muro_cierre)

    # --- Muros laterales largos: ladrillo/terracota uniforme (corregido) ---
    crear_caja("Muro_Lateral_AndenA_Exterior", col_arquitectura,
               pos_doc=(X_MURO_OESTE_ANDEN_A, ALTURA_ARRANQUE / 2, 0),
               size_doc=(0.4, ALTURA_ARRANQUE, LARGO_ESTACION), material=mat_muro_ladrillo)
    crear_caja("Muro_Lateral_AndenB_Exterior", col_arquitectura,
               pos_doc=(X_MURO_ESTE_ANDEN_B, ALTURA_ARRANQUE / 2, 0),
               size_doc=(0.4, ALTURA_ARRANQUE, LARGO_ESTACION), material=mat_muro_ladrillo)

    # --- Techo de vigas (corregido: reemplaza la boveda lisa v1) -----------
    crear_techo_vigas(col_arquitectura,
                       ancho=ANCHO_TOTAL, largo=LARGO_ESTACION,
                       altura=ALTURA_TECHO, separacion=SEPARACION_VIGAS,
                       mat_viga=mat_viga, mat_luz=mat_luz_viga, mat_panel=mat_techo_panel)
    # El techo esta centrado en X=0 por defecto (ver crear_techo_vigas); se
    # recentra al medio del ancho total nuevo desplazando sus hijos.
    _centro_techo_x = (X_MURO_OESTE_ANDEN_A + X_MURO_ESTE_ANDEN_B) / 2.0
    for obj in list(col_arquitectura.objects):
        if obj.name.startswith("Viga_") or obj.name.startswith("LuzViga_") or obj.name == "Techo_Panel":
            obj.location.x += _centro_techo_x

    # --- Foso de vias combinado (Via1 + Via2 juntas, sin muro entre ellas) --
    ancho_fosos = X_ANDEN_B_INICIO - X_VIA1_INICIO
    centro_fosos = (X_VIA1_INICIO + X_ANDEN_B_INICIO) / 2.0
    crear_caja("Foso_Vias", col_arquitectura,
               pos_doc=(centro_fosos, -0.55, 0), size_doc=(ancho_fosos, 1.1, LARGO_ESTACION),
               material=mat_balasto)

    crear_caja("Franja_Naranja_Via1", col_arquitectura,
               pos_doc=(X_VIA1_INICIO + 0.15, -0.05, 0), size_doc=(0.08, 0.05, LARGO_ESTACION),
               material=mat_franja_via_naranja)
    crear_caja("Franja_Naranja_Via2", col_arquitectura,
               pos_doc=(X_ANDEN_B_INICIO - 0.15, -0.05, 0), size_doc=(0.08, 0.05, LARGO_ESTACION),
               material=mat_franja_via_naranja)

    # --- Rieles (2 por via) -------------------------------------------------
    for centro_via, nombre_via in ((X_VIA1_CENTRO, "Via1"), (X_VIA2_CENTRO, "Via2")):
        for signo, lado in ((-1, "A"), (1, "B")):
            crear_caja(f"Riel_{nombre_via}_{lado}", col_arquitectura,
                       pos_doc=(centro_via + signo * GALGA, 0.05, 0),
                       size_doc=(0.1, 0.15, LARGO_ESTACION), material=mat_riel)

    # --- Columnas CILINDRICAS: una fila por anden (corregido: v1/v2 tenian
    # una sola fila central, asumiendo anden unico) --------------------------
    for i, z in enumerate(POSICIONES_COLUMNAS, start=1):
        crear_cilindro(f"Columna_AndenA_{i:02d}", col_arquitectura,
                        pos_doc=(X_ANDEN_A_CENTRO, ALTURA_ARRANQUE / 2, z), radio=0.35,
                        alto_doc=ALTURA_ARRANQUE, material=mat_columna_ladrillo, vertices=16)
        crear_cilindro(f"Columna_AndenB_{i:02d}", col_arquitectura,
                        pos_doc=(X_ANDEN_B_CENTRO, ALTURA_ARRANQUE / 2, z), radio=0.35,
                        alto_doc=ALTURA_ARRANQUE, material=mat_columna_ladrillo, vertices=16)

    # --- Caseta de control (en Anden_A, posicion original) -------------------
    crear_caja("Caseta_Control", col_arquitectura,
               pos_doc=(X_ANDEN_A_CENTRO - 1.0, 1.1, 0), size_doc=(2, 2.2, 2), material=mat_muro_ladrillo)

    # --- Barreras de seguridad en extremos (ambos andenes) -------------------
    for z in (-(MEDIO_LARGO - 1.5), (MEDIO_LARGO - 1.5)):
        etiqueta = "Norte" if z < 0 else "Sur"
        crear_caja(f"Barrera_AndenA_{etiqueta}", col_senaletica,
                   pos_doc=(X_VIA1_INICIO - 0.1, 0.5, z), size_doc=(0.3, 1.0, 0.6), material=mat_reja)
        crear_caja(f"Barrera_AndenB_{etiqueta}", col_senaletica,
                   pos_doc=(X_ANDEN_B_INICIO + 0.1, 0.5, z), size_doc=(0.3, 1.0, 0.6), material=mat_reja)

    # --- Bloqueos ------------------------------------------------------------
    crear_caja("Reja_Escalera_Norte", col_senaletica,
               pos_doc=(X_ANDEN_A_CENTRO, 1.5, -MEDIO_LARGO + 0.2), size_doc=(3, 3, 0.1), material=mat_reja)

    # Via2 (Anden_B) sellada -- el jugador no la necesita para el camino critico
    crear_caja("Reja_Tunel_Via2", col_senaletica,
               pos_doc=(X_VIA2_CENTRO, -0.1, MEDIO_LARGO + 0.1), size_doc=(ANCHO_VIA, 2.0, 0.1),
               material=mat_reja)

    # --- Panel de llegadas (suspendido, cerca del acceso norte, Anden_A) ----
    crear_caja("Panel_Llegadas_Carcasa", col_senaletica,
               pos_doc=(X_ANDEN_A_CENTRO, 3.6, -MEDIO_LARGO + 5), size_doc=(2.5, 0.8, 0.2),
               material=mat_panel_carcasa)
    crear_caja("Panel_Llegadas_Pantalla", col_senaletica,
               pos_doc=(X_ANDEN_A_CENTRO, 3.6, -MEDIO_LARGO + 5 - 0.11), size_doc=(2.2, 0.5, 0.02),
               material=mat_panel_pantalla)

    # --- Punto de descenso a la via (Anden_A -> Via1, camino critico) -------
    crear_caja("Descenso_Via", col_arquitectura,
               pos_doc=(X_VIA1_INICIO - 0.25, -0.3, MEDIO_LARGO - 2.5), size_doc=(1.0, 1.1, 2.0),
               material=mat_piso_manchas)

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

    crear_caja_herramientas("Caja_Herramientas_Rodrigo", col_props,
                             pos_doc=(X_ANDEN_A_CENTRO - 3.0, 0, MEDIO_LARGO - 4), material=mat_toolbox)

    crear_reloj_anden("Reloj_Anden", col_props, pos_doc=(0, 0, -20),
                       mat_carcasa=mat_reloj_carcasa, mat_esfera=mat_reloj_esfera)

    for i, z in enumerate((-40, -2, 40), start=1):
        crear_cartel_colgante(f"Cartel_Baquedano_{i:02d}", col_senaletica,
                                pos_doc=(0, 4.35, z), mat_panel=mat_muro_ladrillo, texto="BAQUEDANO",
                                mat_texto=mat_cartel_texto)

    crear_caja("Nota_Tecnico", col_props, pos_doc=(2.3, 0.46, 0.6),
               size_doc=(0.25, 0.02, 0.18), material=mat_toolbox)

    # Anden_B: props minimos, solo atmosfera (no es camino critico del jugador)
    crear_banca("Banca_AndenB_01", col_props, pos_doc=(X_ANDEN_B_CENTRO + 0.9, 0, -10),
                mat_madera=mat_madera, mat_metal=mat_metal_banca)
    crear_basurero("Basurero_AndenB_01", col_props, pos_doc=(X_ANDEN_B_CENTRO - 0.8, 0, 15),
                   material=mat_basurero)

    total = (len(col_arquitectura.objects) + len(col_senaletica.objects)
             + len(col_props.objects))
    print(f"[LINEA CERO] Estacion completa generada (v2). Objetos totales: {total}. "
          f"Columnas: {len(POSICIONES_COLUMNAS)}. Vigas: {int(LARGO_ESTACION // SEPARACION_VIGAS)}. "
          f"Largo real: {LARGO_ESTACION} m.")


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
