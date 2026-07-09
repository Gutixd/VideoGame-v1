"""
LINEA CERO - Anden Baquedano
Fase 3.3 - Materiales (geometria corregida + boveda real + PBR en Blender)

Ejecutar en modo headless:
    blender --background --python generar_materiales.py

Correcciones respecto al blockout (Fase 3.1) encontradas al armar
colision en Godot, documentadas aqui en vez de en el .md por ser
detalle de implementacion:

  1. El muro sur original (dos piezas sobre las VIAS) bloqueaba el
     punto de descenso. Se reemplaza por un unico muro que cierra
     solo el ANDEN (7 m), dejando ambas vias abiertas hacia sus
     respectivos tuneles, tal como es realmente: las vias siguen,
     el anden no.
  2. Faltaban los muros laterales largos (los que llevan el zocalo
     ceramico + la franja de color, la pieza mas reconocible de la
     estetica Metro Santiago). Se agregan corriendo los 55 m,
     limitando el ancho total de la estacion (14 m).
  3. La reja del tunel este ahora bloquea especificamente la boca de
     la VIA este (no un muro completo), a la altura del foso.
  4. El punto de descenso se realinea con el borde anden/via oeste.
  5. La boveda deja de ser una caja: se genera con bmesh como un arco
     circular segmentado (radio ~21 m) que da un alza de 1.2 m sobre
     el arranque de 4.3 m, resultando en la clave a 5.5 m documentada.

Convencion de coordenadas (igual que en generar_blockout.py):
    X_doc = Este / Oeste       -> Blender X
    Y_doc = Altura (up)        -> Blender Z
    Z_doc = Sur / Norte        -> Blender Y
"""

import bpy
import bmesh
import math
import os

# ---------------------------------------------------------------------------
# Rutas de texturas (reutilizadas de Sala Tecnica + nuevas para esta zona)
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

    unwrap_basico(obj)

    if material:
        obj.data.materials.append(material)

    for col in obj.users_collection:
        col.objects.unlink(obj)
    coleccion.objects.link(obj)
    return obj


def crear_boveda(nombre, coleccion, ancho, largo, altura_arranque, alza, material=None, segmentos=28):
    """Boveda de cañón segmentada (arco circular), no un semicirculo completo.

    ancho: ancho total de la boveda (14 m, cuerda del arco)
    largo: longitud de la estacion (55 m)
    altura_arranque: altura donde el muro se convierte en boveda (4.3 m)
    alza: elevacion de la clave sobre el arranque (1.2 m -> clave a 5.5 m)
    """
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
        if material.use_nodes:
            # La boveda se ve desde abajo -> evitar cull de cara trasera
            material.use_backface_culling = False

    return obj


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

    # --- Materiales ---------------------------------------------------
    mat_hormigon = crear_material_pbr("Hormigon_Boveda", RUTAS["hormigon"],
                                       roughness_default=0.85, uv_scale=(4, 4))
    mat_hormigon_columna = crear_material_pbr("Hormigon_Columna", RUTAS["hormigon"],
                                               tint=(0.75, 0.75, 0.78), roughness_default=0.6,
                                               uv_scale=(1, 2))
    mat_hormigon_muro_cierre = crear_material_pbr("Hormigon_MuroCierre", RUTAS["hormigon"],
                                                   roughness_default=0.85, uv_scale=(3, 2))
    mat_zocalo = crear_material_pbr("Zocalo_Ceramico", RUTAS["ceramica"],
                                     tint=(0.85, 0.8, 0.7), roughness_default=0.3,
                                     uv_scale=(9, 1))
    mat_franja = crear_material_pbr("Franja_Identificadora", RUTAS["ceramica"],
                                     tint=(0.75, 0.55, 0.15), roughness_default=0.35,
                                     uv_scale=(9, 2))
    mat_terrazo = crear_material_pbr("Terrazo_Piso", RUTAS["terrazo"],
                                      roughness_default=0.35, uv_scale=(3, 20))
    mat_balasto = crear_material_pbr("Balasto_Via", RUTAS["balasto"],
                                      roughness_default=0.95, uv_scale=(2, 20))
    mat_riel = crear_material_pbr("Riel_Metalico", RUTAS["metal"],
                                   tint=(0.55, 0.55, 0.58), metallic=0.85,
                                   roughness_default=0.3, uv_scale=(1, 20))
    mat_reja = crear_material_pbr("Reja_Oxidada", RUTAS["metal"],
                                   tint=(0.75, 0.42, 0.22), metallic=0.4,
                                   roughness_default=0.7, uv_scale=(2, 2))
    mat_franja_tactil = crear_material_simple("Franja_Tactil", (0.85, 0.7, 0.05),
                                               metallic=0.0, roughness=0.6)
    mat_panel_carcasa = crear_material_simple("Panel_Carcasa", (0.05, 0.05, 0.06),
                                               metallic=0.3, roughness=0.4)
    mat_panel_pantalla = crear_material_simple("Panel_Pantalla", (0.15, 0.08, 0.0),
                                                emission=(1.0, 0.6, 0.1), emission_strength=2.5)

    # --- Piso -----------------------------------------------------------
    crear_caja("Piso_Anden", col_arquitectura,
               pos_doc=(0, 0, 0), size_doc=(7, 0.2, 55), material=mat_terrazo)

    # Franja tactil (dos tiras finas en los bordes del anden)
    crear_caja("Franja_Tactil_Oeste", col_senaletica,
               pos_doc=(-3.3, 0.01, 0), size_doc=(0.3, 0.02, 55), material=mat_franja_tactil)
    crear_caja("Franja_Tactil_Este", col_senaletica,
               pos_doc=(3.3, 0.01, 0), size_doc=(0.3, 0.02, 55), material=mat_franja_tactil)

    # --- Muros de cierre (norte cierra todo, sur cierra solo el anden) ---
    crear_caja("Muro_Norte", col_arquitectura,
               pos_doc=(0, 2.15, -27.5), size_doc=(14, 4.3, 0.5), material=mat_hormigon_muro_cierre)

    crear_caja("Muro_Sur", col_arquitectura,
               pos_doc=(0, 2.15, 27.5), size_doc=(7, 4.3, 0.5), material=mat_hormigon_muro_cierre)

    # --- Muros laterales largos: zocalo + franja identificadora ---------
    ALTURA_ZOCALO = 1.2
    ALTURA_FRANJA = 4.3 - ALTURA_ZOCALO
    for lado, x in (("Oeste", -7), ("Este", 7)):
        crear_caja(f"Muro_Lateral_{lado}_Zocalo", col_arquitectura,
                   pos_doc=(x, ALTURA_ZOCALO / 2, 0), size_doc=(0.4, ALTURA_ZOCALO, 55),
                   material=mat_zocalo)
        crear_caja(f"Muro_Lateral_{lado}_Franja", col_arquitectura,
                   pos_doc=(x, ALTURA_ZOCALO + ALTURA_FRANJA / 2, 0),
                   size_doc=(0.4, ALTURA_FRANJA, 55), material=mat_franja)

    # --- Boveda real (arco segmentado) -----------------------------------
    crear_boveda("Boveda", col_arquitectura, ancho=14, largo=55,
                 altura_arranque=4.3, alza=1.2, material=mat_hormigon)

    # --- Fosos de via (con balasto) ---------------------------------------
    crear_caja("Foso_Via1", col_arquitectura,
               pos_doc=(-5.25, -0.55, 0), size_doc=(3.5, 1.1, 55), material=mat_balasto)
    crear_caja("Foso_Via2", col_arquitectura,
               pos_doc=(5.25, -0.55, 0), size_doc=(3.5, 1.1, 55), material=mat_balasto)

    # --- Rieles (2 por via) -------------------------------------------------
    galga = 0.7175
    for centro_via, nombre_via in ((-5.25, "Via1"), (5.25, "Via2")):
        for signo, lado in ((-1, "A"), (1, "B")):
            crear_caja(f"Riel_{nombre_via}_{lado}", col_arquitectura,
                       pos_doc=(centro_via + signo * galga, 0.05, 0),
                       size_doc=(0.1, 0.15, 55), material=mat_riel)

    # --- Columnas (9) --------------------------------------------------------
    posiciones_z = [-24, -18, -12, -6, 0, 6, 12, 18, 24]
    for i, z in enumerate(posiciones_z, start=1):
        crear_caja(f"Columna_{i:02d}", col_arquitectura,
                   pos_doc=(0, 2.15, z), size_doc=(0.6, 4.3, 0.6), material=mat_hormigon_columna)

    # --- Caseta de control -----------------------------------------------
    crear_caja("Caseta_Control", col_arquitectura,
               pos_doc=(1.5, 1.1, 0), size_doc=(2, 2.2, 2), material=mat_zocalo)

    # --- Barreras de seguridad en extremos ---------------------------------
    for z in (-26, 26):
        crear_caja(f"Barrera_Oeste_{'Norte' if z < 0 else 'Sur'}", col_senaletica,
                   pos_doc=(-3.4, 0.5, z), size_doc=(0.3, 1.0, 0.6), material=mat_reja)
        crear_caja(f"Barrera_Este_{'Norte' if z < 0 else 'Sur'}", col_senaletica,
                   pos_doc=(3.4, 0.5, z), size_doc=(0.3, 1.0, 0.6), material=mat_reja)

    # --- Bloqueos ------------------------------------------------------------
    crear_caja("Reja_Escalera_Norte", col_senaletica,
               pos_doc=(0, 1.5, -27.3), size_doc=(3, 3, 0.1), material=mat_reja)

    # Corregido: bloquea la VIA este (no un muro completo), a la altura del foso
    crear_caja("Reja_Tunel_Este", col_senaletica,
               pos_doc=(5.25, -0.1, 27.6), size_doc=(3.5, 2.0, 0.1), material=mat_reja)

    # --- Panel de llegadas (suspendido) -------------------------------------
    crear_caja("Panel_Llegadas_Carcasa", col_senaletica,
               pos_doc=(0, 3.6, -3), size_doc=(2.5, 0.8, 0.2), material=mat_panel_carcasa)
    crear_caja("Panel_Llegadas_Pantalla", col_senaletica,
               pos_doc=(0, 3.6, -3.11), size_doc=(2.2, 0.5, 0.02), material=mat_panel_pantalla)

    # --- Punto de descenso a la via (realineado al borde anden/via oeste) ---
    crear_caja("Descenso_Via", col_arquitectura,
               pos_doc=(-3.75, -0.3, 25), size_doc=(1.0, 1.1, 2.0), material=mat_terrazo)

    print(f"[LINEA CERO] Materiales aplicados. Objetos totales: "
          f"{len(col_arquitectura.objects) + len(col_senaletica.objects)}")


# ---------------------------------------------------------------------------
# Guardado y exportacion
# ---------------------------------------------------------------------------

def guardar_y_exportar():
    blend_path = os.path.join(SCRIPT_DIR, "anden_baquedano_materiales.blend")
    glb_dir = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "assets", "models", "anden_baquedano"))
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, "anden_baquedano_materiales.glb")

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
