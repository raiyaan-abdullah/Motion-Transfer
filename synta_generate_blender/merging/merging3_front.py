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
    bpy.ops.mesh.primitive_plane_add(size=35, location=(0, 20, 0))
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
    radius = 25
    
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

def animate_objects_to_center(objects, start_frame, merge_frame):
    """Animates objects to move towards a central location."""
    center_location = (0, 0, 1)
    for obj in objects:
        # Insert initial keyframe
        obj.keyframe_insert(data_path="location", frame=start_frame)
        # Move object to center location
        obj.location = center_location
        # Insert keyframe for merge position
        obj.keyframe_insert(data_path="location", frame=merge_frame)

def scale_object(obj, scale_factor, scale_frame, hold_duration=20):
    """
    Scales an object by a factor, inserts keyframes for the scaling, and holds that scale for a specified duration.
    
    :param obj: The object to be scaled.
    :param scale_factor: The factor by which the object's scale is multiplied.
    :param scale_frame: The frame at which the scaling takes effect.
    :param hold_duration: The number of frames to hold the new scale before any further changes.
    """
    # Ensure the scale before the change is kept up to this point
    obj.keyframe_insert(data_path="scale", frame=scale_frame - 1)

    # Update the object's scale and insert a keyframe
    obj.scale *= scale_factor
    obj.keyframe_insert(data_path="scale", frame=scale_frame)

    # Insert another keyframe to maintain the scale for hold_duration frames
    obj.keyframe_insert(data_path="scale", frame=scale_frame + hold_duration)

def delete_objects_handler(scene, objects_to_delete, delete_after_frame):
    if scene.frame_current >= delete_after_frame:
        for obj in objects_to_delete:
            # Make sure the object still exists before trying to delete it
            if obj.name in bpy.data.objects:
                bpy.data.objects.remove(bpy.data.objects[obj.name], do_unlink=True)
        # After deleting, remove this handler to prevent it from running again
        bpy.app.handlers.frame_change_pre.remove(delete_objects_handler)
        
def setup_delete_handler(objects_to_delete, delete_after_frame):
    # Use a lambda to create a closure that captures the objects to delete and the delete frame
    handler_func = lambda scene: delete_objects_handler(scene, objects_to_delete, delete_after_frame)
    bpy.app.handlers.frame_change_pre.append(handler_func)
    return handler_func  # Return the handler function for potential removal later


# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\merging3_front_id_{i+1}.mp4"
        setup_scene(output_file_path)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()  # Ensure this function is defined elsewhere in your script
        create_background_image(image_path+images[i%10])
        
        color = (random.random(), random.random(), random.random(), 1)
        locations = [(-5, 5, 1), (5, 5, 1), (5, -5, 1), (-5, -5, 1)]

        # Create the first object
        obj1, shape1 = create_random_object_basic_set1(color)
        obj1.location = locations[0]
        objects = [obj1]  # Start a list of objects with the first object

        # Loop to create and position additional objects
        for loc in locations[1:]:
            while True:
                obj, shape = create_random_object_basic_set1(color)
                if shape == shape1:
                    obj.location = loc  # Position it only if the shape matches
                    objects.append(obj)  # Keep track of the created object
                    break  # Exit the loop if a matching object is found
                else:
                    # Properly remove the non-matching object before trying again
                    bpy.data.objects.remove(obj, do_unlink=True)

        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = (0,0,1)
        setup_camera(target)

        start_frame = 1
        merge_frame = 60  # Frame at which objects will merge
        
        animate_objects_to_center(objects, start_frame, merge_frame)
        # Example of calling scale_object with a custom hold duration
        scale_factor = 1.5
        scale_frame = merge_frame - 5  # Scale right after merging
        hold_duration = 20  # Hold the scale for 20 frames

        # Scale obj1 and maintain that scale for hold_duration frames
        scale_object(obj1, scale_factor, scale_frame, hold_duration)


        
        # Calculate the frame after which the other objects should be deleted
        delete_after_frame = scale_frame +1

        # Delete the other three objects, keeping only obj1 (now scaled and representing the merged object)
        handler_func = setup_delete_handler(objects[1:], delete_after_frame)

        # IMPORTANT: Set the scene's start and end frames for rendering
        bpy.context.scene.frame_start = start_frame
        bpy.context.scene.frame_end = scale_frame + hold_duration

        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\merging"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

