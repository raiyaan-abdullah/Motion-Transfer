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
def animate_rising_object_zigzag(obj, start_height, end_height, start_frame, end_frame, lateral_distance, steps):
    """
    Animates an object rising in a zigzag pattern from a start height to an end height.

    Parameters:
    - obj: The object to animate.
    - start_height: The starting Z position.
    - end_height: The ending Z position.
    - start_frame: The frame at which the animation starts.
    - end_frame: The frame at which the animation ends.
    - lateral_distance: The maximum distance the object moves laterally in each zigzag step.
    - steps: The number of zigzag steps during the rise.
    """
    frames_per_step = (end_frame - start_frame) // steps
    vertical_step = (end_height - start_height) / steps
    current_height = start_height
    current_frame = start_frame

    # Ensure the object starts at the specified start height
    obj.location.z = current_height
    obj.keyframe_insert(data_path="location", frame=current_frame, index=2)  # Z-axis

    direction_x = 1  # Start moving in positive X direction
    direction_y = 1  # Start moving in positive Y direction

    for step in range(1, steps + 1):
        # Calculate the next position
        current_height += vertical_step
        lateral_movement_x = (step % 2) * direction_x * lateral_distance  # Alternate movement in X
        lateral_movement_y = ((step + 1) % 2) * direction_y * lateral_distance  # Alternate movement in Y
        direction_x *= -1 if (step % 2) else 1  # Change direction for X every other step
        direction_y *= -1 if ((step + 1) % 2) else 1  # Change direction for Y every other step

        # Move the object for the zigzag effect
        obj.location.x += lateral_movement_x
        obj.location.y += lateral_movement_y
        obj.location.z = current_height

        # Update the frame for the next keyframe
        current_frame += frames_per_step

        # Insert keyframes for the new position
        obj.keyframe_insert(data_path="location", frame=current_frame, index=0)  # X-axis
        obj.keyframe_insert(data_path="location", frame=current_frame, index=1)  # Y-axis
        obj.keyframe_insert(data_path="location", frame=current_frame, index=2)  # Z-axis

    # Optionally, set the scene to end at the last keyframe
    bpy.context.scene.frame_end = current_frame



# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\rising2_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create a random object with glistening material
        obj1 = create_random_object()

        # Adjust the position of obj1 to be above the ground
        obj1.location = (0, 0, 5)   # Start 5 units above the ground

        # Setup camera to focus on the falling object
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = obj1.location  # Focus on the object
        setup_camera(target)

        # Inside your generate_videos function, replace the animate_falling_object call with:
        animate_rising_object_zigzag(obj1, start_height=1, end_height=10, start_frame=1, end_frame=120, lateral_distance=4, steps=7)


        # Render the animation
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\rising"
generate_videos(base_path)

