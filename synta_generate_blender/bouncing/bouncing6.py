import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=45, location=(0, 0, 0))  # Adjust size as needed
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
    radius = 20
    
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

# Animate the object moving into view
def animate_constant_bouncing(obj, start_frame, end_frame, start_height, constant_height, floor_level=0):
    """
    Animates an object to start bouncing from a specific height and then continues bouncing
    at a constant height indefinitely.

    Parameters:
    - obj: The object to animate.
    - start_frame: The frame at which the animation starts.
    - end_frame: The frame at which the animation ends.
    - start_height: The initial starting height of the object.
    - constant_height: The constant height of the bounce maintained after the first bounce.
    - floor_level: The Z-level at which the object bounces.
    """
    scene = bpy.context.scene
    scene.frame_start = start_frame
    scene.frame_end = end_frame

    frames_per_bounce = 30  # Define how many frames each bounce takes
    current_frame = start_frame

    # Initial bounce from start_height to floor_level
    # Peak of the first bounce
    obj.location.z = start_height + floor_level
    obj.keyframe_insert(data_path="location", frame=current_frame)

    # Falling to the floor level
    next_keyframe = current_frame + frames_per_bounce // 2
    obj.location.z = floor_level
    obj.keyframe_insert(data_path="location", frame=next_keyframe)

    # Bouncing back to constant_height
    current_frame += frames_per_bounce
    obj.location.z = constant_height + floor_level
    obj.keyframe_insert(data_path="location", frame=current_frame)

    # Setup for continuous bouncing at constant_height
    while current_frame <= end_frame:
        # Falling back to floor level
        next_keyframe = current_frame + frames_per_bounce // 2
        obj.location.z = floor_level
        obj.keyframe_insert(data_path="location", frame=next_keyframe)

        # Bouncing back to constant_height
        current_frame += frames_per_bounce
        obj.location.z = constant_height + floor_level
        obj.keyframe_insert(data_path="location", frame=current_frame)


# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\bouncing6_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create a random object with glistening material
        obj = create_random_object()

        # Setup camera to focus on the object
        setup_camera(obj)

        # Animate the object bouncing
        animate_constant_bouncing(obj, start_frame=1, end_frame=160, start_height=6, constant_height=4, floor_level=1)

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\bouncing"
generate_videos(base_path)
