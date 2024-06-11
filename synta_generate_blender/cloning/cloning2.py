import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))  # Adjust size as needed
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

# Updated animate_object function to include object cloning and movement
def animate_object(obj):
    start_frame = 1
    clone_start_frame = 30
    end_frame = 60

    # Ensure the original object stays still until the cloning frame
    obj.location.y = 0
    obj.keyframe_insert(data_path="location", frame=start_frame)
    obj.keyframe_insert(data_path="location", frame=clone_start_frame)

    # Create clones at the cloning frame
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.duplicate_move()
    clone1 = bpy.context.active_object
    clone2 = obj

    # Move clones in opposite directions after clone_start_frame
    clone1.location.y += 4  # Move one clone up
    clone2.location.y -= 4  # Move the other clone down
    clone1.keyframe_insert(data_path="location", frame=end_frame)
    clone2.keyframe_insert(data_path="location", frame=end_frame)

# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\cloning1_id_{i+1}.mp4"  # Unique filename for each video
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

        # Add animation, camera, and lighting setup here (omitted for brevity)
        animate_object(obj)

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\cloning"
generate_videos(base_path)
