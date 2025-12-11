import bpy
import math
import random

# ------------------------------------------------------------------
# Config section — tweak these for instant different looks
# ------------------------------------------------------------------
BASE_COLOR = (0.85, 0.18, 0.04, 1)       # warm coppery metal
METALLIC = 1.0
ROUGHNESS_BASE = 0.35                    # only used if you disable the mask
NOISE_SCALE_RANGE = (8.0, 25.0)
COLORRAMP_NARROW = (0.46, 0.50)          # sharp scratches
RANDOM_ROTATION = True
TEST_OBJECT = "monkey"                   # "sphere", "cube", "monkey", "ico"
# ------------------------------------------------------------------

def wipe_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    # Clean up orphaned data
    for _ in range(4):
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

def build_scratch_mask(mat):
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # start from right to left
    x_step = -320
    x = 400

    # ColorRamp — tight band = sharp scratches
    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (x, -150)
    x += x_step
    ramp.color_ramp.elements[0].position = COLORRAMP_NARROW[0]
    ramp.color_ramp.elements[1].position = COLORRAMP_NARROW[1]

    # Noise
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (x, -150)
    x += x_step
    noise.inputs['Scale'].default_value = random.uniform(*NOISE_SCALE_RANGE)
    noise.inputs['Detail'].default_value = 10.0

    # Mapping (random rotation for variety)
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (x, -150)
    x += x_step
    if RANDOM_ROTATION:
        for axis in ('X', 'Y', 'Z'):
            mapping.inputs[f'Rotation'].default_value[ord(axis)-88] = math.radians(random.uniform(0, 360))

    # Texture Coordinate
    coord = nodes.new('ShaderNodeTexCoord')
    coord.location = (x, -150)

    # Connections
    links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])

    return ramp.outputs['Color']

def make_material():
    mat = bpy.data.materials.new(name="ScratchedMetal")
    mat.use_nodes = True

    # Clear default nodes for full control
    mat.node_tree.nodes.clear()

    # Principled BSDF + Output
    bsdf = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Base Color'].default_value = BASE_COLOR
    bsdf.inputs['Metallic'].default_value = METALLIC
    bsdf.inputs['Roughness'].default_value = ROUGHNESS_BASE

    output = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)
    mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Connect scratch mask to roughness
    mask = build_scratch_mask(mat)
    mat.node_tree.links.new(mask, bsdf.inputs['Roughness'])

    return mat

def spawn_test_object():
    if TEST_OBJECT == "monkey":
        bpy.ops.mesh.primitive_monkey_add(size=1.5)
    elif TEST_OBJECT == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32)
    elif TEST_OBJECT == "cube":
        bpy.ops.mesh.primitive_cube_add(size=2)
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5)

    obj = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    return obj

# ------------------------------------------------------------------
# Run everything
# ------------------------------------------------------------------
wipe_scene()
material = make_material()
obj = spawn_test_object()

# Assign material
if obj.data.materials:
    obj.data.materials[0] = material
else:
    obj.data.materials.append(material)

print("Procedural scratched metal ready!")
