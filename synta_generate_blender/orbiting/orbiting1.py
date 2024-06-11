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
    radius = 20
    
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
def animate_object(obj, central_obj):
    start_frame = 1
    end_frame = 120  # Shorten this to increase speed
    radius = 5  # Distance from central object
    
    for frame in range(start_frame, end_frame + 1):
        angle = 2 * math.pi * (frame / end_frame)  # Full circle
        x = central_obj.location.x + radius * math.cos(angle)  # Cosine for X
        y = central_obj.location.y - radius * math.sin(angle)  # Negative sine for clockwise direction
        
        obj.location = (x, y, 1)  # Keep the same Z as central object
        obj.keyframe_insert(data_path="location", frame=frame)
    
    bpy.context.scene.frame_end = end_frame  # Ensure the scene ends at the right frame

def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\orbiting1_id_{i+1}.mp4"  # Adjust path as necessary

        # Setup scene for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        central_obj = create_random_object()  # Central object that others will orbit
        central_obj.location = (0, 0, 1)  # Place at the center of the scene
        orbiting_obj = create_random_object()  # Assuming this creates a new object

        # Setup camera to focus on the central object
        setup_camera(central_obj)

        # Add animation to the orbiting object
        animate_object(orbiting_obj, central_obj)

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\orbiting"
generate_videos(base_path)
