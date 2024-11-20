import bpy
import random
import math 
from basic_setup_appearance import *

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

# Animate the object moving into view
def animate_falling_object(obj, start_height, end_height, start_frame, end_frame):
    """
    Animates an object falling from a start height to an end height.

    Parameters:
    - obj: The object to animate.
    - start_height: The starting Z position.
    - end_height: The ending Z position.
    - start_frame: The frame at which the animation starts.
    - end_frame: The frame at which the animation ends.
    """
    # Ensure the object starts at the specified start height
    obj.location.z = start_height
    # Insert a keyframe for the starting position at the start frame
    obj.keyframe_insert(data_path="location", frame=start_frame, index=2)  # Index 2 for the Z-axis

    # Move the object to the end height
    obj.location.z = end_height
    # Insert a keyframe for the ending position at the end frame
    obj.keyframe_insert(data_path="location", frame=end_frame, index=2)  # Index 2 for the Z-axis

    # Optionally, set the scene to end at the end frame for the animation
    bpy.context.scene.frame_end = end_frame



# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\falling1_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Create a random object with glistening material
        obj1 = create_random_object_set1()

        # Adjust the position of obj1 to be above the ground
        obj1.location = (0, 0, 5)   # Start 5 units above the ground

        # Setup camera to focus on the falling object
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = obj1.location  # Focus on the object
        setup_camera(target)

        # Animate obj1 falling
        animate_falling_object(obj1, start_height=8, end_height=1, start_frame=1, end_frame=60)

        # Render the animation
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\falling"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

