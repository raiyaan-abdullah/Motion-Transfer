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
    radius = 35
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = -(radius * math.sin(angle) + target.location.y)
    z = random.uniform(0, 5)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving from start_location to end_location
def animate_object(obj, waypoints, frames):
    """
    Animates an object through specified waypoints at given frames.

    Parameters:
    - obj: The object to animate.
    - waypoints: A list of locations [(x, y, z), ...] through which the object will move.
    - frames: A list of frames corresponding to each waypoint.
    """
    for waypoint, frame in zip(waypoints, frames):
        obj.location = waypoint
        obj.keyframe_insert(data_path="location", frame=frame)

# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\not_colliding5_front_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Stationary objects' locations
        static_obj_locations = [
            (-5, -5, 5),  # Position for the first stationary object
            (5, -5, 4),   # Position for the second stationary object
            (0, 5, -4)     # Position for the third stationary object
        ]

        # Create and place stationary objects
        for loc in static_obj_locations:
            static_obj = create_random_object_set2()
            static_obj.location = loc

        # Moving object's animation path waypoints and frames
        waypoints_moving_obj = [(-20, 0, 0), (0, 0, 0), (20, 0, 0)]
        frames_moving_obj = [1, 60, 120]  # Start, mid (close approach), end frames

        # Create and animate the moving object
        moving_obj = create_random_object_set2()
        animate_object(moving_obj, waypoints_moving_obj, frames_moving_obj)

        # Setup camera to focus on the central action area
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = (0, 0, 1)  # Focus on the center of action
        setup_camera(target)

        # Adjust scene's end frame to accommodate the last animation
        bpy.context.scene.frame_end = frames_moving_obj[-1] + 10  # Add a buffer to ensure full exit is captured

        # Render the animation
        bpy.ops.render.render(animation=True)

        # Cleanup the target object after rendering
        bpy.data.objects.remove(target)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\not_colliding"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
