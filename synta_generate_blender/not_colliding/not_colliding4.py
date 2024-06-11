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
    radius = 30
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(20, 30)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving from start_location to end_location
def animate_circular_motion(obj, initial_location, radius, start_frame, end_frame, clockwise=True):
    """
    Correctly animates an object in a circular motion starting exactly at the initial location.
    The circular path's center is calculated to ensure the initial location is on the path.

    Parameters:
    - obj: The object to animate.
    - initial_location: The initial location (x, y, z) of the object.
    - radius: Radius of the circular path.
    - start_frame, end_frame: Frame range for the animation.
    - clockwise: True for clockwise motion, False for counter-clockwise.
    """
    # Assuming the circular motion is in the XY plane
    # Adjust the calculation if the motion plane is different
    angle_offset = math.atan2(initial_location[1], initial_location[0])

    num_frames = end_frame - start_frame
    for i in range(num_frames + 1):
        frame = start_frame + i
        angle = 2 * math.pi * (i / num_frames) * (1 if clockwise else -1) + angle_offset

        # Calculate the new location based on circular motion
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = initial_location[2]  # Keeping Z constant for a horizontal circle

        bpy.context.scene.frame_set(frame)
        obj.location = (x, y, z)
        obj.keyframe_insert(data_path="location", frame=frame)


# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\not_colliding4_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Initial locations for the two objects at the edge of their respective circles
        initial_location_obj1 = (10, 3, 1)  # Starting on the left
        initial_location_obj2 = (3, 0, 1)   # Starting on the right

        # Radius for the circular motion
        radius1 = 5
        radius2 = 8

        # Create the first moving object and animate it in a clockwise circular motion
        moving_obj1 = create_random_object()
        moving_obj1.location = initial_location_obj1
        animate_circular_motion(moving_obj1, initial_location_obj1, radius1, 1, 120, clockwise=True)

        # Create the second moving object and animate it in a counter-clockwise circular motion
        moving_obj2 = create_random_object()
        moving_obj2.location = initial_location_obj2
        animate_circular_motion(moving_obj2, initial_location_obj2, radius2, 1, 120, clockwise=False)

        # Setup camera to focus on the central action area
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = (0, 0, 1)  # Focus on the center of action
        setup_camera(target)

        # Adjust scene's end frame to accommodate the last animation
        bpy.context.scene.frame_end = 120

        # Render the animation
        bpy.ops.render.render(animation=True)

        # Cleanup the target object after rendering
        bpy.data.objects.remove(target)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\not_colliding"
generate_videos(base_path)
