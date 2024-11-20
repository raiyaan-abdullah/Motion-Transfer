import bpy
import random
import math

#Keep in C:\Program Files\Blender Foundation\Blender 4.0\4.0\scripts\addons

# Set rendering engine and output settings
def setup_scene(output_file_path):
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.fps = 24
    bpy.context.scene.render.filepath = output_file_path
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'

# Function to generate a random color
def random_color():
    return (random.random(), random.random(), random.random(), 1)

def create_glossy_mix_node_group():
    # Create new node group
    group = bpy.data.node_groups.new(name="GlossyMixGroup", type="ShaderNodeTree")

    # Define interface
    color_input = group.interface.new_socket(
        name="Base Color",
        description="Base color for the glossy shaders",
        in_out='INPUT',
        socket_type='NodeSocketColor'
    )
    color_input.default_value = (random.random(), random.random(), random.random(), 1)  # Random color

    shader_output = group.interface.new_socket(
        name="Shader Output",
        description="Output shader",
        in_out='OUTPUT',
        socket_type='NodeSocketShader'
    )

    # Create nodes inside the group
    nodes = group.nodes
    links = group.links

    group_in = nodes.new(type='NodeGroupInput')
    group_out = nodes.new(type='NodeGroupOutput')

    glossy_bsdf1 = nodes.new(type='ShaderNodeBsdfGlossy')
    glossy_bsdf2 = nodes.new(type='ShaderNodeBsdfGlossy')
    mix_shader = nodes.new(type='ShaderNodeMixShader')
    fresnel = nodes.new(type='ShaderNodeFresnel')

    # Configure nodes
    glossy_bsdf1.inputs['Roughness'].default_value = 0.447
    glossy_bsdf1.inputs['Anisotropy'].default_value = 0.25
    glossy_bsdf2.inputs['Roughness'].default_value = 0.1
    glossy_bsdf2.inputs['Anisotropy'].default_value = 0.25
    fresnel.inputs['IOR'].default_value = 1.45
    mix_shader.inputs['Fac'].default_value = 0.6  # Mix factor influenced by Fresnel

    # Position nodes for clarity
    group_in.location = (-350, 0)
    fresnel.location = (-150, 100)
    glossy_bsdf1.location = (-150, -100)
    glossy_bsdf2.location = (0, -100)
    mix_shader.location = (200, 0)
    group_out.location = (350, 0)

    # Link nodes
    links.new(group_in.outputs['Base Color'], glossy_bsdf1.inputs['Color'])
    links.new(group_in.outputs['Base Color'], glossy_bsdf2.inputs['Color'])
    links.new(fresnel.outputs[0], mix_shader.inputs[0])
    links.new(glossy_bsdf1.outputs[0], mix_shader.inputs[1])
    links.new(glossy_bsdf2.outputs[0], mix_shader.inputs[2])
    links.new(mix_shader.outputs[0], group_out.inputs['Shader Output'])

    return group



# Function to create random object and apply glistening material
def create_random_object_set1():
    objects = ['CUBE', 'CONE', 'PYRAMID', 'PRISM']
    object_type = random.choice(objects)

    # Add object to the scene based on random choice
    if object_type == 'CUBE':
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    elif object_type == 'CONE':
        bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, location=(0, 0, 1))
    elif object_type == 'PYRAMID':
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=1, depth=2, location=(0, 0, 1))
    elif object_type == 'PRISM':
        # Create a triangular prism (as an example)
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=2, location=(0, 0, 1))
        prism_obj = bpy.context.object

        # Optionally, adjust the prism to align one of the vertices with the world axis, or perform other transformations

        # Smooth the prism shape
        bpy.ops.object.shade_smooth()


    # Assuming 'create_glossy_mix_node_group' is already defined and called
    glossy_mix_group = create_glossy_mix_node_group()

    # Create a new material
    material = bpy.data.materials.new(name="GlossyMixMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # Clear any existing nodes
    nodes.clear()

    # Add a shader node group to use the custom node group
    group_node = nodes.new('ShaderNodeGroup')
    # Assign the node tree of the created group to this shader node group
    group_node.node_tree = glossy_mix_group

    # Connect the group output to the material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    links = material.node_tree.links
    links.new(group_node.outputs['Shader Output'], material_output.inputs['Surface'])

    obj = bpy.context.object


    # Assign the material to the object
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

    return obj

# Function to create random object and apply glistening material
def create_random_object_set2():
    objects = ['SPHERE', 'CYLINDER', 'TORUS', 'CAPSULE']
    object_type = random.choice(objects)

    # Add object to the scene based on random choice
    if object_type == 'SPHERE':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
    elif object_type == 'CYLINDER':
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 1))
    elif object_type == 'TORUS':
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, 1))
    elif object_type == 'CAPSULE':
        # Create cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 1))
        cylinder = bpy.context.object
        
        # Create top sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 2))
        top_sphere = bpy.context.object
        
        # Create bottom sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        bottom_sphere = bpy.context.object

        # Select all parts of the capsule
        bpy.ops.object.select_all(action='DESELECT')
        cylinder.select_set(True)
        top_sphere.select_set(True)
        bottom_sphere.select_set(True)
        bpy.context.view_layer.objects.active = cylinder

        # Join the parts into a single object
        bpy.ops.object.join()


    # Assuming 'create_glossy_mix_node_group' is already defined and called
    glossy_mix_group = create_glossy_mix_node_group()

    # Create a new material
    material = bpy.data.materials.new(name="GlossyMixMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # Clear any existing nodes
    nodes.clear()

    # Add a shader node group to use the custom node group
    group_node = nodes.new('ShaderNodeGroup')
    # Assign the node tree of the created group to this shader node group
    group_node.node_tree = glossy_mix_group

    # Connect the group output to the material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    links = material.node_tree.links
    links.new(group_node.outputs['Shader Output'], material_output.inputs['Surface'])

    obj = bpy.context.object


    # Assign the material to the object
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

    return obj

def add_point_light(location, rotation, color, radius, energy, max_bounces, cast_shadow, importance_sampling):
    bpy.ops.object.light_add(type='POINT', radius=radius, location=location)
    light = bpy.context.object
    light.rotation_euler = rotation
    light.data.color = color
    light.data.energy = energy
    light.data.cycles.max_bounces = max_bounces
    light.data.cycles.cast_shadow = cast_shadow
    light.data.cycles.use_multiple_importance_sampling = importance_sampling

def add_sun_light(location, rotation, color, energy, angle_degrees, max_bounces, cast_shadow, importance_sampling):
    bpy.ops.object.light_add(type='SUN', location=location)
    light = bpy.context.object
    light.rotation_euler = rotation
    light.data.color = color
    light.data.energy = energy
    light.data.angle = angle_degrees * (3.14159265 / 180)
    light.data.cycles.max_bounces = max_bounces
    light.data.cycles.cast_shadow = cast_shadow
    light.data.cycles.use_multiple_importance_sampling = importance_sampling

def add_spot_light(location, rotation, color, energy, radius, spot_size_degrees, spot_blend, max_bounces, cast_shadow, importance_sampling):
    bpy.ops.object.light_add(type='SPOT', radius=radius, location=location)
    light = bpy.context.object
    light.rotation_euler = rotation
    light.data.color = color
    light.data.energy = energy
    light.data.spot_size = spot_size_degrees * (3.14159265 / 180)
    light.data.spot_blend = spot_blend
    light.data.cycles.max_bounces = max_bounces
    light.data.cycles.cast_shadow = cast_shadow
    light.data.cycles.use_multiple_importance_sampling = importance_sampling

def add_area_light(location, rotation, shape, size, color, energy, max_bounces, cast_shadow, importance_sampling, spread_degrees):
    bpy.ops.object.light_add(type='AREA', location=location)
    light = bpy.context.object
    light.rotation_euler = rotation
    light.data.shape = shape
    light.data.size = size
    light.data.color = color
    light.data.energy = energy
    light.data.cycles.max_bounces = max_bounces
    light.data.cycles.cast_shadow = cast_shadow
    light.data.cycles.use_multiple_importance_sampling = importance_sampling
    light.data.spread = spread_degrees * (3.14159265 / 180)

def setup_lights():

    add_point_light(location=(11, -6, 25), rotation=(math.radians(45), 0, 0), color=(1, 1, 1), radius=0.1, energy=0.45, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(11, -6, 25), rotation=(math.radians(45), 0, 0), color=(1, 1, 1), energy=0.45, angle_degrees=11.4, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(11, -6, 25), rotation=(math.radians(45), 0, 0), color=(1, 1, 1), energy=0.45, radius=0.1, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(11, -6, 25), rotation=(math.radians(45), 0, 0), shape='SQUARE', size=0.1, color=(1, 1, 1), energy=0.45, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)

    add_point_light(location=(-10, 3, 6), rotation=(math.radians(45), 0, 0), color=(1, 1, 1), radius=1.0, energy=2, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(-10, 3, 6), rotation=(math.radians(45), 0, 0), color=(1, 1, 1), energy=15, angle_degrees=10, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(-10, 3, 6), rotation=(math.radians(45), 0, 0), color=(1, 1, 1), energy=2, radius=1.0, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(-10, 3, 6), rotation=(math.radians(45), 0, 0), shape='SQUARE', size=1.0, color=(1, 1, 1), energy=2, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)
    
    add_point_light(location=(-5, -40, 3), rotation=(math.radians(20), 0, 0), color=(1, 1, 1), radius=0.5, energy=3, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(-5, -40, 3), rotation=(math.radians(20), 0, 0), color=(1, 1, 1), energy=3, angle_degrees=53.1, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(-5, -40, 3), rotation=(math.radians(20), 0, 0), color=(1, 1, 1), energy=3, radius=0.5, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(-5, -40, 3), rotation=(math.radians(20), 0, 0), shape='SQUARE', size=0.5, color=(1, 1, 1), energy=3, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)
    
    #add_point_light(location=(6, -20, 4), rotation=(math.radians(0), 0, 0), color=(1, 0.93, 0.81), radius=0.5, energy=4, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    #add_sun_light(location=(6, -20, 4), rotation=(math.radians(0), 0, 0), color=(1, 0.93, 0.81), energy=4, angle_degrees=53.1, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    #add_spot_light(location=(6, -20, 4), rotation=(math.radians(0), 0, 0), color=(1, 0.93, 0.81), energy=4, radius=0.5, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    #add_area_light(location=(6, -20, 4), rotation=(math.radians(0), 0, 0), shape='SQUARE', size=0.5, color=(1, 0.93, 0.81), energy=4, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)

def look_at(obj, target):
    direction = target.location - obj.location
    # Point the camera's '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()