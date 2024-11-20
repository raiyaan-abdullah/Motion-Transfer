import bpy
import random
import math 
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

# Animate the object moving into view
def animate_object(obj):
    start_frame = 1
    # Reduced number of frames to increase speed of movement
    end_frame = 120  # Shorten this to increase speed

    # Initial position of the object (within camera view but at one side)
    obj.location = (-5, 0, 1)  # Adjust as needed to start within frame
    obj.keyframe_insert(data_path="location", frame=start_frame)
    
    # Ending position of the object (move to another location within the camera's view)
    obj.location = (5, 0, 1)  # Move to the opposite side within the camera's view
    obj.keyframe_insert(data_path="location", frame=end_frame)

    # Set the scene to end at the end_frame to make the animation quick
    bpy.context.scene.frame_end = end_frame

# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\moving_in_a_path1_front_id_{i+1}.mp4"  # Unique filename for each video
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

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\moving_in_a_path"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
