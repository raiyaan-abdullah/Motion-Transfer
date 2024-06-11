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
    angles = [70, 75, 80, 90, 100, 105, 110]
    
    # Randomly select one of the angles for the camera position
    angle = math.radians(random.choice(angles))
    
    # Define a radius for how far from the target the camera should be
    radius = 40
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(5, 15)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_object(obj, central_obj):
    start_frame = 1
    end_frame = 120
    radius = 5
    
    for frame in range(start_frame, end_frame + 1):
        angle = 2 * math.pi * (frame / end_frame)
        # Cosine for Y to keep motion on a vertical plane around Z
        x = central_obj.location.x + radius * math.cos(angle)
        # Sine for Z, adjust for vertical plane orbit
        z = central_obj.location.z + radius * math.sin(angle)
        
        obj.location = (x, central_obj.location.y, z)
        obj.keyframe_insert(data_path="location", frame=frame)
    
    bpy.context.scene.frame_end = end_frame

def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\orbiting5_id_{i+1}.mp4"

        setup_scene(output_file_path)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        central_obj = create_random_object()
        central_obj.location = (0, 0, 6)  # Elevated central object
        orbiting_obj = create_random_object()
        orbiting_obj.location = (0, 0, 1)

        setup_camera(central_obj)
        animate_object(orbiting_obj, central_obj)
        bpy.ops.render.render(animation=True)


# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\orbiting"
generate_videos(base_path)
