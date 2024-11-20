import bpy
import random
import math 
from mathutils import Matrix, Vector
from basic_setup_appearance import *

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

# Updated animate_object function to include object cloning and movement
def animate_object(obj):
    initial_start_frame = 30  # Initial start frame for the first clone's animation
    clone_movement_duration = 10  # Duration for each clone's movement
    time_between_clones = 10  # Time between the start of each clone's movement

    directions = [(5, 0, 0), (-5, 0, 0)]  # Directions for each clone's movement

    for i in range(3):  # Loop to create two clones
        if i == 0:
            clone = obj  # The first "clone" is actually the original object
        else:
            # Duplicate the original object for subsequent clones
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
            clone = bpy.context.active_object

            if i == 2:  # Apply a different color to the second clone
                # Create a new material with a random color
                glossy_mix_group = create_glossy_mix_node_group()
                material = bpy.data.materials.new(name=f"Clone_{i}_Material")
                material.use_nodes = True
                nodes = material.node_tree.nodes
                nodes.clear()
                group_node = nodes.new('ShaderNodeGroup')
                group_node.node_tree = glossy_mix_group
                material_output = nodes.new('ShaderNodeOutputMaterial')
                links = material.node_tree.links
                links.new(group_node.outputs['Shader Output'], material_output.inputs['Surface'])
                clone.data.materials.clear()
                clone.data.materials.append(material)

                # Initially set the second clone to be not visible
                clone.hide_render = True
                clone.keyframe_insert(data_path="hide_render", frame=initial_start_frame - 1)

        # Calculate the start frame for this clone's movement
        clone_start_frame = initial_start_frame + (clone_movement_duration + time_between_clones) * (i - 1)
        clone_end_frame = clone_start_frame + clone_movement_duration  # End frame for the clone's movement

        if i > 0:
            # Make the clone visible right before it starts moving
            if i == 2:
                clone.hide_render = False
                clone.keyframe_insert(data_path="hide_render", frame=clone_start_frame - 1)

            # Set the clone's initial location keyframe at its current position
            clone.keyframe_insert(data_path="location", frame=clone_start_frame)
            direction = directions[(i - 1) % len(directions)]  # Direction to move the clone
            move_vector = Vector(direction)  # Convert the direction to a vector
            clone.location += move_vector  # Update the clone's location
            clone.keyframe_insert(data_path="location", frame=clone_end_frame)  # Keyframe for the new location



# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\cloning5_front_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Create a random object with glistening material
        obj = create_random_object_set1()

        # Setup camera to focus on the object
        setup_camera(obj)

        # Add animation, camera, and lighting setup here (omitted for brevity)
        animate_object(obj)
        bpy.context.scene.frame_end = 120

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\cloning"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
