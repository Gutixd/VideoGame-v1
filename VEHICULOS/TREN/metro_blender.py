# -*- coding: utf-8 -*-
# ============================================================================
#  METRO EN BLENDER  ·  generador de escena (estilo Metro de Santiago)
# ----------------------------------------------------------------------------
#  Crea: tren teal de 3 coches, estacion con anden + linea amarilla, tunel,
#        interior con asientos naranjos + barras, cabina de conduccion con
#        panel de botones, camaras y animacion de llegada del tren.
#
#  COMO USARLO:
#    1) Abre Blender (3.6 o 4.x).
#    2) Ve a la pestana  "Scripting"  (arriba).
#    3) Boton  "New"  -> pega TODO este archivo.
#    4) Boton  "Run Script"  (o Alt+P).
#    5) Vuelve a  "Layout",  presiona  0  (vista de camara) y  barra espaciadora
#       para reproducir la animacion.
#
#  Camaras creadas:  Cam_Exterior (activa), Cam_Interior, Cam_Cabina.
#  Para cambiar de camara: seleccionala en el Outliner y Ctrl+Numpad0.
# ============================================================================

import bpy
import bmesh
from math import radians

# ----------------------------------------------------------------------------
#  CONFIG  (cambia estos valores a gusto)
# ----------------------------------------------------------------------------
N_COCHES        = 3       # numero de vagones
CONSTRUIR_INT   = True    # interior (asientos, barras, luz)
CONSTRUIR_CAB   = True    # cabina de conduccion
ANIMAR          = True    # animar la llegada del tren

# Colores (RGB 0-1)
TEAL     = (0.090, 0.660, 0.700)   # cuerpo del tren (turquesa)
DARK     = (0.090, 0.100, 0.120)   # bajos / marcos
GRAY     = (0.500, 0.520, 0.550)   # frontal gris
GLASS    = (0.020, 0.040, 0.060)   # vidrios (oscuros)
ORANGE   = (0.950, 0.450, 0.060)   # asientos
METAL    = (0.700, 0.720, 0.750)   # barras / metal
CONCRETE = (0.560, 0.510, 0.430)   # anden
TILE     = (0.640, 0.560, 0.440)   # muro de la estacion
YELLOW   = (0.950, 0.760, 0.050)   # linea de seguridad
CABBLUE  = (0.620, 0.720, 0.820)   # consola cabina
RED      = (0.800, 0.050, 0.050)
GREEN    = (0.050, 0.700, 0.100)
YELLOWB  = (0.900, 0.800, 0.050)
WHITE    = (0.900, 0.900, 0.900)

# Dimensiones del coche (metros)
CAR_LEN  = 17.0
CAR_W    = 2.60
HALF_W   = CAR_W / 2.0
GAP      = 0.30                       # separacion entre coches
STEP     = CAR_LEN + GAP              # avance de un coche al siguiente

# ----------------------------------------------------------------------------
#  UTILIDADES
# ----------------------------------------------------------------------------
_MATS = {}

def clear_scene():
    """Borra todo lo de la escena actual."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras):
        for b in list(coll):
            if b.users == 0:
                coll.remove(b)
    _MATS.clear()

def mat_solid(name, color, metallic=0.0, rough=0.5):
    if name in _MATS:
        return _MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if b is None:
        b = m.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        out = next((n for n in m.node_tree.nodes if n.type == 'OUTPUT_MATERIAL'), None)
        if out:
            m.node_tree.links.new(b.outputs[0], out.inputs['Surface'])
    b.inputs['Base Color'].default_value = (*color, 1.0)
    b.inputs['Metallic'].default_value   = metallic
    b.inputs['Roughness'].default_value  = rough
    _MATS[name] = m
    return m

def mat_emit(name, color, strength=2.0):
    if name in _MATS:
        return _MATS[name]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    em  = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value    = (*color, 1.0)
    em.inputs['Strength'].default_value = strength
    nt.links.new(em.outputs['Emission'], out.inputs['Surface'])
    _MATS[name] = m
    return m

def box(name, dims, loc, mat=None, bevel=None, rot=None):
    """Crea un cubo con dimensiones reales en metros."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if rot:  o.rotation_euler = rot
    if mat:  o.data.materials.append(mat)
    if bevel:
        md = o.modifiers.new('bevel', 'BEVEL')
        md.width = bevel[0]
        md.segments = bevel[1]
        md.limit_method = 'ANGLE'
    return o

def _iter_fcurves(obj):
    """Devuelve las F-curves de un objeto en Blender 3.x-5.x (API antigua y nueva)."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    act = ad.action
    if hasattr(act, 'fcurves') and len(act.fcurves) > 0:
        for fc in act.fcurves:
            yield fc
        return
    # Blender 4.4+ : accion en capas (layers > strips > channelbag > fcurves)
    for layer in getattr(act, 'layers', []):
        for strip in getattr(layer, 'strips', []):
            for slot in getattr(act, 'slots', []):
                cb = strip.channelbag(slot) if hasattr(strip, 'channelbag') else None
                if cb:
                    for fc in cb.fcurves:
                        yield fc

def cyl(name, radius, depth, loc, mat=None, rot=None, verts=20):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth,
                                        location=loc, vertices=verts)
    o = bpy.context.active_object
    o.name = name
    if rot:  o.rotation_euler = rot
    if mat:  o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return o

# ----------------------------------------------------------------------------
#  UN COCHE (vagon)
# ----------------------------------------------------------------------------
def build_car(cx, is_lead):
    P = []
    m_teal  = mat_solid('teal',  TEAL,  0.15, 0.25)
    m_dark  = mat_solid('dark',  DARK,  0.2, 0.5)
    m_glass = mat_solid('glass', GLASS, 0.3, 0.1)
    m_gray  = mat_solid('gray',  GRAY,  0.1, 0.5)
    m_metal = mat_solid('metal', METAL, 0.8, 0.3)

    # Cuerpo principal (teal, con cantos redondeados)
    P.append(box("Cuerpo", (CAR_LEN, CAR_W, 2.20), (cx, 0, 2.40),
                 m_teal, bevel=(0.16, 3)))
    # Bajos oscuros
    P.append(box("Bajos", (CAR_LEN, CAR_W + 0.02, 0.55), (cx, 0, 1.05), m_dark))
    # Banda negra de ventanas (envuelve el coche)
    P.append(box("Banda", (CAR_LEN - 0.6, CAR_W + 0.05, 0.95), (cx, 0, 2.70), m_dark))

    # Ventanas y puertas en ambos costados
    door_x   = [-5.3, 0.0, 5.3]
    window_x = [-7.4, -2.65, 2.65, 7.4]
    for side in (-1, 1):
        y = side * (HALF_W + 0.02)
        for wx in window_x:
            P.append(box("Ventana", (2.0, 0.06, 1.00), (cx + wx, y, 2.70), m_glass))
        for dx in door_x:
            P.append(box("Puerta",     (1.40, 0.05, 1.85), (cx + dx, y, 2.20), m_dark))
            P.append(box("PuertaVidr", (1.15, 0.07, 0.70), (cx + dx, y, 2.85), m_glass))

    # Bogies + ruedas (2 por coche)
    for bx in (-5.0, 5.0):
        P.append(box("Bogie", (2.6, 2.2, 0.5), (cx + bx, 0, 0.70), m_dark))
        for ax in (-1.0, 1.0):
            for wy in (-1.05, 1.05):
                P.append(cyl("Rueda", 0.42, 0.20, (cx + bx + ax, wy, 0.42),
                             m_metal, rot=(radians(90), 0, 0)))

    # Detalles del frontal (solo coche lider): MORRO redondeado
    if is_lead:
        fx = cx + CAR_LEN / 2.0
        # Nariz tapereada con techo rebajado (parabrisas inclinado), via bmesh
        V = [(fx - 0.3, -1.28, 1.00), (fx - 0.3, 1.28, 1.00),
             (fx - 0.3,  1.28, 3.45), (fx - 0.3, -1.28, 3.45),
             (fx + 1.6, -1.05, 1.35), (fx + 1.6, 1.05, 1.35),
             (fx + 0.95, 1.05, 3.15), (fx + 0.95, -1.05, 3.15)]
        Fc = [(0, 1, 5, 4), (3, 7, 6, 2), (0, 4, 7, 3),
              (1, 2, 6, 5), (4, 5, 6, 7), (0, 3, 2, 1)]
        me = bpy.data.meshes.new('NarizMesh')
        nose = bpy.data.objects.new('Nariz', me)
        bpy.context.collection.objects.link(nose)
        bm = bmesh.new()
        vv = [bm.verts.new(v) for v in V]
        bm.verts.ensure_lookup_table()
        for f in Fc:
            bm.faces.new([vv[i] for i in f])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(me)
        bm.free()
        for poly in me.polygons:
            poly.use_smooth = True
        nose.data.materials.append(m_teal)
        mdn = nose.modifiers.new('bv', 'BEVEL')
        mdn.width = 0.18
        mdn.segments = 3
        mdn.limit_method = 'ANGLE'
        P.append(nose)
        # Parabrisas inclinado
        P.append(box("Parabrisas", (0.08, 1.95, 1.15), (fx + 1.22, 0, 2.72),
                     m_glass, rot=(0, radians(-32), 0)))
        # Luces de posicion rojo / blanco / rojo
        for ly, lc, ln in ((-0.75, RED, "R"), (0.0, WHITE, "W"), (0.75, RED, "R2")):
            P.append(box("Marca" + ln, (0.10, 0.42, 0.24), (fx + 1.64, ly, 1.55),
                         mat_solid('marca_' + ln, lc)))
        # Faros
        for hy in (-0.9, 0.9):
            P.append(box("Faro", (0.12, 0.26, 0.18), (fx + 1.45, hy, 2.05),
                         mat_emit('faro', WHITE, 3.0)))
    return P

# ----------------------------------------------------------------------------
#  INTERIOR (dentro de un coche)
# ----------------------------------------------------------------------------
def build_interior(cx):
    P = []
    m_floor  = mat_solid('in_floor', (0.60, 0.60, 0.62))
    m_orange = mat_solid('asiento', ORANGE, 0.0, 0.4)
    m_metal  = mat_solid('metal', METAL, 0.8, 0.3)
    P.append(box("In_Piso",  (CAR_LEN - 0.5, CAR_W - 0.4, 0.05), (cx, 0, 1.36), m_floor))
    P.append(box("In_Techo", (CAR_LEN - 0.5, CAR_W - 0.6, 0.08), (cx, 0, 3.34),
                 mat_emit('in_luz', (1.0, 0.95, 0.85), 1.4)))
    for side in (-1, 1):
        for i, sx in enumerate((-6, -3, 0, 3, 6)):
            P.append(box("Asiento", (1.2, 0.5, 0.10), (cx + sx, side * 0.85, 1.75), m_orange))
            P.append(box("Respaldo", (1.2, 0.1, 0.55), (cx + sx, side * 1.05, 2.05), m_orange))
    for px in (-6, -3, 0, 3, 6):
        P.append(cyl("Barra", 0.04, 2.0, (cx + px, 0, 2.35), m_metal))
    return P

# ----------------------------------------------------------------------------
#  CABINA DE CONDUCCION
# ----------------------------------------------------------------------------
def build_cab(cx):
    P = []
    fx = cx + CAR_LEN / 2.0
    bx = fx - 1.5
    m_cab   = mat_solid('cab_blue', CABBLUE, 0.1, 0.3)
    m_metal = mat_solid('metal', METAL, 0.8, 0.3)
    m_dark  = mat_solid('dark', DARK, 0.2, 0.5)
    # Consola inclinada
    P.append(box("Cab_Consola", (2.4, 1.1, 0.14), (bx, 0, 2.00), m_cab, rot=(radians(-16), 0, 0)))
    P.append(box("Cab_Base", (2.4, 1.1, 0.9), (bx, 0, 1.45), m_cab))
    # Botones (rojo/amarillo/verde)
    botones = [(-0.75, RED), (-0.55, YELLOWB), (-0.35, GREEN),
               (0.35, RED), (0.55, GREEN), (0.75, RED)]
    for i, (yy, col) in enumerate(botones):
        P.append(cyl("Cab_Boton%d" % i, 0.05, 0.05, (bx + 0.05, yy, 2.14),
                     mat_solid('btn_%d' % i, col, 0.0, 0.3)))
    # Palancas
    for i, lx in enumerate((-0.20, 0.20)):
        P.append(cyl("Cab_Palanca%d" % i, 0.03, 0.4, (bx + 0.15, lx, 2.28), m_metal))
        P.append(cyl("Cab_Perilla%d" % i, 0.06, 0.06, (bx + 0.15, lx, 2.48), m_dark))
    # Manometro
    P.append(cyl("Cab_Manometro", 0.12, 0.03, (bx + 0.05, 0.0, 2.16),
                 mat_solid('gauge', WHITE), rot=(radians(-16), 0, 0)))
    # Pantalla (emisiva)
    P.append(box("Cab_Pantalla", (0.05, 0.9, 0.5), (fx - 0.25, 0.85, 2.75),
                 mat_emit('screen', (0.05, 0.05, 0.02), 0.6)))
    return P

# ----------------------------------------------------------------------------
#  ESTACION + TUNEL
# ----------------------------------------------------------------------------
def build_station():
    m_conc  = mat_solid('concreto', CONCRETE, 0.0, 0.7)
    m_tile  = mat_solid('muro', TILE, 0.0, 0.6)
    m_yellow= mat_solid('amarillo', YELLOW, 0.0, 0.4)
    m_dark  = mat_solid('tunel', (0.03, 0.03, 0.035), 0.0, 0.8)
    m_metal = mat_solid('metal', METAL, 0.8, 0.3)

    # Anden (lado -Y, frente a las puertas)
    box("Anden", (90, 5.0, 1.0), (0, -5.2, 0.5), m_conc)
    box("LineaAmarilla", (90, 0.4, 0.02), (0, -2.85, 1.01), m_yellow)
    # Muro de la estacion (detras del tren, lado +Y)
    box("Muro", (90, 0.3, 6.5), (0, 3.4, 3.2), m_tile)
    # Techo / boveda oscura
    box("Techo", (90, 14, 0.4), (0, -1.5, 6.6), m_dark)
    # Cama de via
    box("Via", (90, 5.5, 0.15), (0, 0, 0.05), m_dark)
    for ry in (-0.72, 0.72):
        box("Riel", (90, 0.10, 0.10), (0, ry, 0.12), m_metal)

    # Cartel "SAN PABLO"
    box("CartelFondo", (3.2, 0.05, 0.7), (10, 3.24, 3.9), mat_solid('cartel', (0.75, 0.10, 0.10)))
    bpy.ops.object.text_add(location=(10.0, 3.20, 3.72))
    t = bpy.context.active_object
    t.name = "SanPablo"
    t.data.body = "SAN PABLO"
    t.data.size = 0.5
    t.data.extrude = 0.01
    t.data.align_x = 'CENTER'
    t.rotation_euler = (radians(90), 0, 0)
    t.scale = (-1, 1, 1)   # voltea horizontal para que se lea de frente
    t.data.materials.append(mat_emit('texto', WHITE, 1.2))

# ----------------------------------------------------------------------------
#  CAMARAS  /  LUCES  /  MUNDO
# ----------------------------------------------------------------------------
def add_camera(name, loc, target, lens=28):
    tgt = bpy.data.objects.new(name + "_obj", None)
    bpy.context.collection.objects.link(tgt)
    tgt.location = target
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = loc
    c = cam.constraints.new('TRACK_TO')
    c.target = tgt
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'
    return cam

def add_light(name, loc, energy, size, ltype='AREA', parent=None):
    ld = bpy.data.lights.new(name, ltype)
    ld.energy = energy
    if ltype == 'AREA':
        ld.size = size
    else:
        ld.shadow_soft_size = size
    lo = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(lo)
    lo.location = loc
    if parent:
        lo.parent = parent
        lo.matrix_parent_inverse = parent.matrix_world.inverted()
    return lo

def setup_world():
    w = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.012, 0.012, 0.015, 1.0)
        bg.inputs['Strength'].default_value = 0.5

def setup_engine():
    scn = bpy.context.scene
    for eng in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE'):
        try:
            scn.render.engine = eng
            break
        except TypeError:
            continue

# ============================================================================
#  CONSTRUCCION PRINCIPAL
# ============================================================================
def main():
    clear_scene()
    setup_engine()
    setup_world()

    train_parts = []

    # Posiciones de los coches: el lider (indice 0) queda hacia +X
    cxs = [i * -STEP + (N_COCHES - 1) * STEP for i in range(N_COCHES)]
    lead_cx = cxs[0]
    mid_cx  = cxs[len(cxs) // 2]

    for i, cx in enumerate(cxs):
        train_parts += build_car(cx, is_lead=(i == 0))

    if CONSTRUIR_INT:
        train_parts += build_interior(mid_cx)
    if CONSTRUIR_CAB:
        train_parts += build_cab(lead_cx)

    # Estacion (estatica, no se mueve con el tren)
    build_station()

    # Raiz del tren (para mover y animar todo junto)
    root = bpy.data.objects.new("Tren_Root", None)
    bpy.context.collection.objects.link(root)
    root.location = (0, 0, 0)
    for o in train_parts:
        o.parent = root
        o.matrix_parent_inverse = root.matrix_world.inverted()

    lead_front = lead_cx + CAR_LEN / 2.0

    # Luces de la estacion
    add_light("Luz_Anden", (0, -3, 7.0), 4000, 12)
    add_light("Luz_Frente", (lead_front + 9, -8, 6.0), 5000, 8)
    add_light("Luz_Relleno", (-15, -6, 6.0), 1500, 10)

    # Luces DENTRO del tren (se mueven con el, EEVEE no rebota la emision)
    if CONSTRUIR_INT:
        for i, dx in enumerate((-6, -2, 2, 6)):
            add_light("InLuz_%d" % i, (mid_cx + dx, 0, 3.05), 2600, 1.2,
                      ltype='POINT', parent=root)
    if CONSTRUIR_CAB:
        add_light("CabLuz", (lead_front - 1.5, 0, 3.05), 450, 1.8, parent=root)

    # Camaras
    cam_ext = add_camera("Cam_Exterior", (lead_front + 15, -11, 4.2),
                         (lead_front - 4, -1.2, 2.5), lens=30)
    add_camera("Cam_Interior", (mid_cx + 6, 0.0, 1.95),
               (mid_cx - 6, 0.0, 1.85), lens=20)
    add_camera("Cam_Cabina", (lead_front - 3.3, 0.0, 2.9),
               (lead_front - 1.2, 0.0, 1.95), lens=20)
    bpy.context.scene.camera = cam_ext

    # Exposicion y calidad de render
    bpy.context.scene.view_settings.exposure = 0.35
    try:
        bpy.context.scene.eevee.taa_render_samples = 32
    except Exception:
        pass

    # Animacion: el tren entra desde +X y se detiene
    if ANIMAR:
        scn = bpy.context.scene
        scn.frame_start = 1
        scn.frame_end = 120
        root.location.x = 55.0
        root.keyframe_insert('location', index=0, frame=1)
        root.location.x = 0.0
        root.keyframe_insert('location', index=0, frame=90)
        root.keyframe_insert('location', index=0, frame=120)
        # Suaviza la frenada (ease out) - compatible con Blender 3.x-5.x
        for fc in _iter_fcurves(root):
            for kp in fc.keyframe_points:
                kp.interpolation = 'BEZIER'
                kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
        scn.frame_set(90)

    print("=" * 60)
    print(" Metro generado.  Coches: %d" % N_COCHES)
    print(" Vista de camara: presiona 0 en el visor 3D.")
    print(" Reproduce con la barra espaciadora.")
    print("=" * 60)


main()
