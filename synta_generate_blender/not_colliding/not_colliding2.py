import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))  # Adjust size as needed
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
    radius = 25
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(10, 20)  # Adjust the Z to change the height of the camera
    
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
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\not_colliding2_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create and place the stationary object
        stationary_obj = create_random_object()
        stationary_obj.location = (0, -2, 1)  # Position the stationary object

        # Define the animation path waypoints and frames for the moving object
        waypoints_moving_obj = [(-20, 2, 1), (0, 2, 1), (20, 2, 1)]
        frames = [1, 60, 120]  # Start, mid (close approach), end frames

        # Create and animate the moving object
        moving_obj = create_random_object()
        animate_object(moving_obj, waypoints_moving_obj, frames)

        # Setup camera to focus on the central action area
        avg_location = (0, 0, 1)  # Focus on the center of action
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = avg_location
        setup_camera(target)

        # Adjust scene's end frame to accommodate the last animation
        bpy.context.scene.frame_end = frames[-1] + 10  # Add a buffer to ensure full exit is captured

        # Render the animation
        bpy.ops.render.render(animation=True)

        # Cleanup the target object after rendering
        bpy.data.objects.remove(target)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\not_colliding"
generate_videos(base_path)
