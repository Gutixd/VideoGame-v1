import bpy, math, os

base_dir = os.path.dirname(os.path.abspath(__file__))
blend_path = os.path.join(base_dir, "personaje.blend")
bpy.ops.wm.open_mainfile(filepath=blend_path)

scene = bpy.context.scene
cam_data = bpy.data.cameras.new("PreviewCam")
cam_obj = bpy.data.objects.new("PreviewCam", cam_data)
scene.collection.objects.link(cam_obj)
cam_obj.location = (0, -2.6, 1.05)
cam_obj.rotation_euler = (math.radians(90), 0, 0)
cam_data.lens = 50
scene.camera = cam_obj

sun = bpy.data.lights.new("Sun", type='SUN')
sun.energy = 3.0
sun_obj = bpy.data.objects.new("Sun", sun)
scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(55), 0, math.radians(35))

fill = bpy.data.lights.new("Fill", type='SUN')
fill.energy = 1.2
fill_obj = bpy.data.objects.new("Fill", fill)
scene.collection.objects.link(fill_obj)
fill_obj.rotation_euler = (math.radians(70), 0, math.radians(-120))

scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 700
scene.render.resolution_y = 1000
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.9, 0.9, 0.9, 1.0)

out_path = os.path.join(base_dir, "preview.png")
scene.render.filepath = out_path
bpy.ops.render.render(write_still=True)
print("Preview guardado en:", out_path)
