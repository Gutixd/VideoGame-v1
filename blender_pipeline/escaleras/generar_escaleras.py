"""
LINEA CERO - Generador de ESCALERA PERFECTA (metro)
Modelado 100% en Blender (bpy), export .glb Y-up para Godot.

Escalera solida con escalones identicos (huella/contrahuella constantes),
rellena por debajo (no escalones flotantes) y con descanso plano arriba.
Topologia limpia: la silueta lateral (unica cara concava) se triangula;
los laterales quedan en quads. Sin huecos, sin caras internas.

Ejecutar headless:
    blender --background --python generar_escaleras.py

Parametros (ajustables): ancho, huella, contrahuella, numero de escalones,
descanso. Con los valores por defecto: 20 escalones de 15cm x 30cm =
3.0 m de altura, 6.0 m de avance, 3.0 m de ancho, descanso de 1.4 m.
Origen en la base-frente-centro (comodo para posicionar en la escena).
"""

import bpy
import bmesh
import os

# ---------------------------------------------------------------------------
# Parametros de la escalera
# ---------------------------------------------------------------------------
ANCHO = 3.0            # ancho (eje X)
HUELLA = 0.30          # profundidad de cada escalon (run)
CONTRAHUELLA = 0.15    # altura de cada escalon (rise)
N_ESCALONES = 20       # cantidad de escalones
DESCANSO = 1.4         # descanso plano al final (0 = sin descanso)


def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for m in list(bpy.data.meshes):
        if m.users == 0:
            bpy.data.meshes.remove(m)


def perfil_lateral():
    """Silueta solida de la escalera en el plano (Y=avance, Z=altura).

    Recorre: base-frente -> sube en zig-zag por los escalones -> descanso
    -> base-atras -> cierra. Poligono simple (no auto-intersecta).
    """
    pts = [(0.0, 0.0)]  # base-frente
    for i in range(N_ESCALONES):
        y = i * HUELLA
        z = (i + 1) * CONTRAHUELLA
        pts.append((y, z))              # sube la contrahuella
        pts.append((y + HUELLA, z))     # avanza la huella
    top_y = N_ESCALONES * HUELLA
    top_z = N_ESCALONES * CONTRAHUELLA
    if DESCANSO > 0.0:
        pts.append((top_y + DESCANSO, top_z))  # borde trasero del descanso
        top_y += DESCANSO
    pts.append((top_y, 0.0))            # base-atras
    return pts


def construir_escalera(nombre="Escalera_Perfecta"):
    perfil = perfil_lateral()
    bm = bmesh.new()

    # Cara lateral en X = -ANCHO/2, luego se extruye +ANCHO en X.
    x0 = -ANCHO / 2.0
    verts = [bm.verts.new((x0, y, z)) for (y, z) in perfil]
    cara = bm.faces.new(verts)

    ret = bmesh.ops.extrude_face_region(bm, geom=[cara])
    verts_ext = [e for e in ret['geom'] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts_ext, vec=(ANCHO, 0.0, 0.0))

    # Triangular solo las caras concavas (las dos siluetas laterales);
    # los laterales rectos quedan en quads limpios.
    ngons = [f for f in bm.faces if len(f.verts) > 4]
    if ngons:
        bmesh.ops.triangulate(bm, faces=ngons)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    mesh = bpy.data.meshes.new(nombre + "_Mesh")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(nombre, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def guardar_y_exportar(obj):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(base_dir, "escalera_perfecta.blend")
    glb_dir = os.path.normpath(os.path.join(base_dir, "..", "..", "assets", "models", "escaleras"))
    os.makedirs(glb_dir, exist_ok=True)
    glb_path = os.path.join(glb_dir, "escalera_perfecta.glb")

    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"[LINEA CERO] .blend guardado: {blend_path}")

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_apply=True,
    )
    print(f"[LINEA CERO] .glb exportado: {glb_path}")


if __name__ == "__main__":
    limpiar_escena()
    bpy.context.scene.unit_settings.system = 'METRIC'
    escalera = construir_escalera()
    altura = N_ESCALONES * CONTRAHUELLA
    avance = N_ESCALONES * HUELLA + DESCANSO
    print(f"[LINEA CERO] Escalera perfecta: {N_ESCALONES} escalones de "
          f"{HUELLA*100:.0f}x{CONTRAHUELLA*100:.0f}cm | altura {altura:.2f}m | "
          f"avance {avance:.2f}m | ancho {ANCHO:.2f}m")
    guardar_y_exportar(escalera)
