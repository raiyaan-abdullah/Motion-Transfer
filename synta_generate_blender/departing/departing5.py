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

# Animate the object moving from start_location to end_location
def animate_object(obj, start_location, end_location, start_frame=1, end_frame=60):
    obj.location = start_location
    obj.keyframe_insert(data_path="location", frame=start_frame)
    obj.location = end_location
    obj.keyframe_insert(data_path="location", frame=end_frame)

# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\departing5_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Object that is already in the scene
        static_obj = create_random_object()
        static_obj.location = (-4, 4, 1)  # Centered in the scene

        # Object that will animate into the scene
        # Define start location further from the center and end location
        start_location = (0, 1, 1)
        end_location = (0, -20, 1)

        # Create and animate the object
        animated_obj = create_random_object()  # Create a random object
        animate_object(animated_obj, start_location, end_location)

        # Setup camera to focus on the general area where action happens
        # Here, focusing between the static and animated object's final position
        avg_end_location = ((static_obj.location.x + start_location[0]) / 2,
                            (static_obj.location.y + start_location[1]) / 2,
                            (static_obj.location.z + start_location[2]) / 2)
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = avg_end_location
        setup_camera(target)

        # Render the animation
        bpy.ops.render.render(animation=True)

        # Cleanup the target object after rendering
        bpy.data.objects.remove(target)


# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\departing"
generate_videos(base_path)
