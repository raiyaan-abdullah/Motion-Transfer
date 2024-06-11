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
    radius = 35
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(25, 40)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

def animate_bouncing_ball(ball):
    frame1 = 1
    frame2 = 10
    frame3 = 20
    frame4 = 30
    frame5 = 40
    frame6 = 42
    frame7 = 50
    frame8 = 70
    frame9 = 90
    frame10 = 110

    # Set frame range
    bpy.context.scene.frame_start = frame1
    bpy.context.scene.frame_end = frame10 + 10

    # Initial position
    ball.location = (0, -8, 5)
    ball.keyframe_insert(data_path="location", frame=frame1)

    # First bounce down to height 1
    ball.location = (0, -4, 1)
    ball.keyframe_insert(data_path="location", frame=frame2)

    # Bounce back up to height 5
    ball.location = (0, 0, 5)
    ball.keyframe_insert(data_path="location", frame=frame3)

    # Bounce back up to height 5
    ball.location = (0, 4, 1)
    ball.keyframe_insert(data_path="location", frame=frame4)

    # Bounce back up to height 5
    ball.location = (0, 8, 5)
    ball.keyframe_insert(data_path="location", frame=frame5)

    # Bounce back up to height 5
    ball.location = (0, 9, 5)
    ball.keyframe_insert(data_path="location", frame=frame6)

    # Bounce back up to height 5
    ball.location = (0, 7, 1)
    ball.keyframe_insert(data_path="location", frame=frame7)

    # Bounce back up to height 5
    ball.location = (0, 2, 5)
    ball.keyframe_insert(data_path="location", frame=frame8)

    # Bounce back up to height 5
    ball.location = (0, -2, 1)
    ball.keyframe_insert(data_path="location", frame=frame9)

    # Bounce back up to height 5
    ball.location = (0, -6, 1)
    ball.keyframe_insert(data_path="location", frame=frame10)


# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\bouncing4_id_{i + 1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create a random object with glistening material
        obj = create_random_object()

        # Setup camera to focus on the object
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = (0,0,0)
        setup_camera(target)

        # Animate the object bouncing
        animate_bouncing_ball(obj)


        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\bouncing"
generate_videos(base_path)
