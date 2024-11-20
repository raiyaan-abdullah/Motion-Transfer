import bpy
import random
import math 
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



def create_random_object_basic_set1(color):
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

# Function to create a background image BSDF
def create_background_image(image_path):
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 20, 0))
    background_plane = bpy.context.object
    background_plane.name = 'Background'
    background_plane.rotation_euler = (math.radians(90), 0, 0)
    
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
    angles = [75, 80, 85, 90, 95, 100, 105]
    
    # Randomly select one of the angles for the camera position
    angle = math.radians(random.choice(angles))
    
    # Define a radius for how far from the target the camera should be
    radius = 30
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = -(radius * math.sin(angle) + target.location.y)
    z = random.uniform(5, 10)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

def animate_objects(obj1, obj2, start_frame, end_frame):
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    
    obj1_initial_location = obj1.location.copy()
    obj2_initial_location = obj2.location.copy()
    
    # Moving towards each other
    obj1_end_location = obj1_initial_location.lerp(obj2_initial_location, 0.5)  # Midpoint
    obj2_end_location = obj1_end_location
    
    # Keyframes for starting locations
    obj1.location = obj1_initial_location
    obj1.keyframe_insert(data_path="location", frame=start_frame)
    obj2.location = obj2_initial_location
    obj2.keyframe_insert(data_path="location", frame=start_frame)
    
    # Keyframes for end locations (merged position)
    obj1.location = obj1_end_location
    obj1.keyframe_insert(data_path="location", frame=end_frame)
    obj2.location = obj2_end_location
    obj2.keyframe_insert(data_path="location", frame=end_frame)

def merge_objects(obj1, obj2, merge_frame):
    bpy.context.scene.frame_set(merge_frame)
    
    # Assuming obj1 and obj2 are at the same location now
    obj1.select_set(True)
    obj2.select_set(True)
    bpy.context.view_layer.objects.active = obj1  # obj1 is the active object
    
    # Join objects (obj2 into obj1)
    bpy.ops.object.join()
    
    # Optionally, rename the merged object
    obj1.name = "MergedObject"



# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\merging1_front_id_{i+1}.mp4"
        setup_scene(output_file_path)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()  # Ensure this function is defined elsewhere in your script
        create_background_image(image_path+images[i%10])
        
        color = (random.random(), random.random(), random.random(), 1)

        # Create the first object
        obj1, obj1_type = create_random_object_basic_set1(color)

        # Try creating the second object until it matches the first in type
        obj2, obj2_type = create_random_object_basic_set1(color)

        while obj2_type != obj1_type:
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all to avoid accidental deletion
            bpy.data.objects.remove(obj2, do_unlink=True)
            obj2, obj2_type = create_random_object_basic_set1(color)

            
        obj1.location = (-4, 0, 1)
        obj2.location = (4, 0, 1)

        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = (0,0,1)
        setup_camera(target)

        start_frame = 1
        end_frame = 60
        animate_objects(obj1, obj2, start_frame, end_frame)

        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\merging"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

