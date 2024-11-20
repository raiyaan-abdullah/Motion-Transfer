import bpy
import random
import math 
import mathutils
from basic_setup_appearance import *

def create_glossy_mix_node_group(color):
    # Create new node group
    group = bpy.data.node_groups.new(name="GlossyMixGroup", type="ShaderNodeTree")

    # Define interface
    color_input = group.interface.new_socket(
        name="Base Color",
        description="Base color for the glossy shaders",
        in_out='INPUT',
        socket_type='NodeSocketColor'
    )
    color_input.default_value = color

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



def create_random_object_basic_set2(color):
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
    glossy_mix_group = create_glossy_mix_node_group(color)

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

    return obj, object_type

def create_background_image(image_path):
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    background_plane = bpy.context.object
    background_plane.name = 'Background'
    
    material = bpy.data.materials.new(name="BackgroundMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = 1.0
    
    
    tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(image_path)
    
    emission_node = material.node_tree.nodes.new('ShaderNodeEmission')
    emission_node.inputs['Strength'].default_value = 2.0  # Adjust this value to control brightness
    
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
    
    background_plane.data.materials.append(material)

def setup_camera(target):
    # Define 6 distinct angles around the target, in radians
    angles = [0, math.pi / 3, 2 * math.pi / 3, math.pi, 4 * math.pi / 3, 5 * math.pi / 3]
    
    # Randomly select one of the angles for the camera position
    angle = random.choice(angles)
    
    # Define a radius for how far from the target the camera should be
    radius = 30
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(15, 25)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

def setup_animation(obj_slow, obj_fast, start_frame, catch_up_frame, end_frame, move_direction):
    """
    Animate two objects where one catches up to the other. Upon catching up, the faster
    object is removed, simulating a merge.
    
    :param obj_slow: The slower-moving object.
    :param obj_fast: The faster-moving object that catches up and is then removed.
    :param start_frame: The frame where the animation starts.
    :param catch_up_frame: The frame where the faster object catches up and merges.
    :param end_frame: The frame where the animation ends.
    :param move_direction: The vector indicating the direction and distance of movement.
    """
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Calculate positions
    slow_initial_location = obj_slow.location
    fast_initial_location = slow_initial_location - move_direction * 0.5  # Start behind
    merge_location = slow_initial_location + move_direction * 0.5
    final_location = slow_initial_location + move_direction

    # Slow object animation
    obj_slow.keyframe_insert(data_path="location", frame=start_frame)
    obj_slow.location = final_location
    obj_slow.keyframe_insert(data_path="location", frame=end_frame)

    # Fast object animation
    obj_fast.keyframe_insert(data_path="location", frame=start_frame)
    obj_fast.location = merge_location
    obj_fast.keyframe_insert(data_path="location", frame=catch_up_frame)

    # Setup a handler to delete the fast object at catch-up frame
    def delete_fast_object(scene):
        if scene.frame_current == catch_up_frame:
            bpy.data.objects.remove(obj_fast, do_unlink=True)
            # Remove the handler after executing
            bpy.app.handlers.frame_change_pre.remove(delete_fast_object)

    # Add the handler
    bpy.app.handlers.frame_change_pre.append(delete_fast_object)


# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\merging2_id_{i+1}.mp4"
        setup_scene(output_file_path)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()  # Ensure this function is defined elsewhere in your script
        create_background_image(image_path+images[i%10])
        
        color = (random.random(), random.random(), random.random(), 1)

        # Create the first object
        obj1, obj1_type = create_random_object_basic_set2(color)

        # Try creating the second object until it matches the first in type
        obj2, obj2_type = create_random_object_basic_set2(color)

        while obj2_type != obj1_type:
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all to avoid accidental deletion
            bpy.data.objects.remove(obj2, do_unlink=True)
            obj2, obj2_type = create_random_object_basic_set2(color)

            
        
        obj1.location = (0, 0, 1)
        obj2.location = (-4, 0, 1)


        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = (0,0,1)
        setup_camera(target)

        # Animation settings
        start_frame = 1
        catch_up_frame = 30  # Adjust the frame where fast object catches up to slow object
        end_frame = 60
        move_direction = mathutils.Vector((4, 0, 0))  # Direction and distance of movement

        setup_animation(obj1, obj2, start_frame, catch_up_frame, end_frame, move_direction)

        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\merging"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

