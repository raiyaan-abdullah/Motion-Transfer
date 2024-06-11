import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))  # Adjust size as needed
    ground_plane = bpy.context.object
    ground_plane.name = 'Ground'
    # Optional: Adjust the ground material
    if not bpy.data.materials.get("GroundMaterial"):
        ground_material = bpy.data.materials.new(name="GroundMaterial")
    else:
        ground_material = bpy.data.materials["GroundMaterial"]
    ground_material.diffuse_color = (0.8, 0.8, 0.8, 1)  # Light grey color
    if ground_plane.data.materials:
        ground_plane.data.materials[0] = ground_material
    else:
        ground_plane.data.materials.append(ground_material)

def setup_camera(target):
    # Define 6 distinct angles around the target, in radians
    angles = [0, math.pi / 3, 2 * math.pi / 3, math.pi, 4 * math.pi / 3, 5 * math.pi / 3]
    
    # Randomly select one of the angles for the camera position
    angle = random.choice(angles)
    
    # Define a radius for how far from the target the camera should be
    radius = 40
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(15, 35)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_falling_diagonal(obj, start_position, end_position, start_frame, end_frame):
    """
    Animates an object falling in a straight line from a start position to an end position.

    Parameters:
    - obj: The object to animate.
    - start_position: The starting position as a tuple (x, y, z).
    - end_position: The ending position as a tuple (x, y, z).
    - start_frame: The frame at which the animation starts.
    - end_frame: The frame at which the animation ends.
    """
    # Ensure the object starts at the specified start position
    obj.location = start_position
    # Insert a keyframe for the starting position at the start frame
    obj.keyframe_insert(data_path="location", frame=start_frame)

    # Move the object to the end position
    obj.location = end_position
    # Insert a keyframe for the ending position at the end frame
    obj.keyframe_insert(data_path="location", frame=end_frame)

    # Optionally, set the scene to end at the end frame for the animation
    bpy.context.scene.frame_end = end_frame



# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\falling3_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create a random object with glistening material
        obj1 = create_random_object()


        # Setup camera to focus on the falling object
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = obj1.location  # Focus on the object
        setup_camera(target)

        # Inside your generate_videos function, replace the animate_falling_object call with:
        animate_falling_diagonal(obj1, start_position=(8, 1, 8), end_position=(-7, 0, 1), start_frame=1, end_frame=60)


        # Render the animation
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\falling"
generate_videos(base_path)

