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



def create_random_object_set1(color):
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
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 20, 0))
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

def setup_initial_object_and_final_object(initial_obj, other_obj_type, color, location=(0, 0, 1)):

    final_obj, final_obj_type = create_random_object_set1(color)  # Create any random object
    while final_obj_type != other_obj_type: #the hollow center of Torus does not create good animation
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all to avoid accidental deletion
        bpy.data.objects.remove(final_obj, do_unlink=True)
        final_obj, final_obj_type = create_random_object_set1(color)         


    final_obj.location = location

    return initial_obj, final_obj


def animate_transformation(initial_obj, final_obj, start_frame, end_frame):
    # Set scene's frame range
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame

    # Insert initial keyframes for both objects at their starting scale
    initial_obj.scale = (1, 1, 1)  # Ensure the initial object is visible
    initial_obj.keyframe_insert(data_path="scale", frame=start_frame)
    
    final_obj.scale = (0.2, 0.2, 0.2)  # Make sure the final object is visible from the start
    final_obj.keyframe_insert(data_path="scale", frame=start_frame)

    # Set keyframes at the end frame where the initial object is minimized
    initial_obj.scale = (0.001, 0.001, 0.001)
    initial_obj.keyframe_insert(data_path="scale", frame=end_frame)

    # Ensure the final_obj grows to a noticeable size by the end
    final_obj.scale = (1, 1, 1)
    final_obj.keyframe_insert(data_path="scale", frame=end_frame)




# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\changing_shape5_front_id_{i+1}.mp4"
        setup_scene(output_file_path)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()  # Ensure this function is defined elsewhere in your script
        create_background_image(image_path+images[i%10])
        
        color1 = (random.random(), random.random(), random.random(), 1)
        color2 = (random.random(), random.random(), random.random(), 1)

        initial_obj1, obj_type1 = create_random_object_set1(color1)  # Create any random object
        while obj_type1 == "TORUS": #the hollow center of Torus does not create good animation
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all to avoid accidental deletion
            bpy.data.objects.remove(initial_obj1, do_unlink=True)
            initial_obj1, obj_type1 = create_random_object_set1(color1)            
    
        # Now assume the initial_obj is at the center, or move it there
        initial_obj1.location = (-2, -2, 1)
        

        
        initial_obj2, obj_type2 = create_random_object_set1(color2)  # Create any random object
        while obj_type2 == obj_type1: #the hollow center of Torus does not create good animation
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all to avoid accidental deletion
            bpy.data.objects.remove(initial_obj2, do_unlink=True)
            initial_obj2, obj_type2 = create_random_object_set1(color2)            
    
        # Now assume the initial_obj is at the center, or move it there
        initial_obj2.location = (2, 2, 1)

        # Setup the final object alongside the initial object
        initial_obj1, final_obj1 = setup_initial_object_and_final_object(initial_obj1, obj_type2, color1, initial_obj1.location)
        
        # Setup the final object alongside the initial object
        initial_obj2, final_obj2 = setup_initial_object_and_final_object(initial_obj2, obj_type1, color2, initial_obj2.location)
        

        
        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = (0,0,1)
        setup_camera(target)

        # Animate the transformation
        animate_transformation(initial_obj1, final_obj1, start_frame=1, end_frame=60)

        # Animate the transformation
        animate_transformation(initial_obj2, final_obj2, start_frame=1, end_frame=60)

        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\changing_shape"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

