import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=25, location=(0, 0, 0))  # Adjust size as needed
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
    z = random.uniform(15, 25)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_object_in_L_shape(obj, start_pos, end_pos, start_frame, mid_frame, end_frame):
    """
    Animates an object moving in an 'L' shaped path from start_pos to end_pos.
    
    Parameters:
    obj (bpy.types.Object): The object to animate.
    start_pos (tuple): The starting position of the object (x, y, z).
    end_pos (tuple): The ending position of the object (x, y, z).
    start_frame (int): The frame at which the animation starts.
    mid_frame (int): The frame at which the object finishes the first leg of the 'L' and starts the second.
    end_frame (int): The frame at which the animation ends.
    """
    # Initial position
    obj.location = start_pos
    obj.keyframe_insert(data_path="location", frame=start_frame)

    # Midpoint - finish the first leg of the 'L' shape
    mid_pos = (end_pos[0], start_pos[1], start_pos[2])  # Change in x-axis, keep y and z from start
    obj.location = mid_pos
    obj.keyframe_insert(data_path="location", frame=mid_frame)
    
    # End position - complete the 'L' shape
    obj.location = end_pos
    obj.keyframe_insert(data_path="location", frame=end_frame)

def animate_two_objects_switching_positions():
    # Create two objects


    # Render the animation
    bpy.ops.render.render(animation=True)


# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\moving_in_a_path4_id_{i+1}.mp4"
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()


        obj1 = create_random_object()
        obj2 = create_random_object()

        # Object positions
        start_pos_obj1 = (3, 9, 1)
        end_pos_obj1 = (-3, -9, 1)
        start_pos_obj2 = (-3, -9, 1)
        end_pos_obj2 = (3, 9, 1)

        # Animation frames
        start_frame = 1
        mid_frame = 30
        end_frame = 60

        # Animate objects
        animate_object_in_L_shape(obj1, start_pos_obj1, end_pos_obj1, start_frame, mid_frame, end_frame)
        animate_object_in_L_shape(obj2, start_pos_obj2, end_pos_obj2, start_frame, mid_frame, end_frame)

        # Camera and lighting setup
        target = bpy.data.objects.new("Target", None)  # A target for the camera to look at
        bpy.context.collection.objects.link(target)
        target.location = (0, 0, 0)
        setup_camera(target)
        setup_lights()

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\moving_in_a_path"
generate_videos(base_path)
