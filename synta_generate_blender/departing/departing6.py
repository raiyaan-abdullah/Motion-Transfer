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

# Animate the object moving from start_location to end_location
def animate_object(obj, enter_location, stay_location, exit_location, enter_frame, start_stay_frame, end_stay_frame, exit_frame):
    # Object enters the scene
    obj.location = enter_location
    obj.keyframe_insert(data_path="location", frame=enter_frame)
    
    # Object moves to the stay location
    obj.location = stay_location
    obj.keyframe_insert(data_path="location", frame=start_stay_frame)

    # Ensure the object stays by reinforcing its stay location with another keyframe
    # This keyframe marks the end of the stay period but doesn't move the object
    obj.location = stay_location
    obj.keyframe_insert(data_path="location", frame=end_stay_frame)
    
    # Object exits
    obj.location = exit_location
    obj.keyframe_insert(data_path="location", frame=exit_frame)

# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\departing6_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Object that is already in the scene
        static_obj = create_random_object()
        static_obj.location = (0, 3, 1)  # Centered in the scene

        # Define locations for the animated object
        enter_location = (0, -3, 1)
        stay_location = (0, -40, 1)
        exit_location = (0, -3, 1)  # Exit in the opposite direction

        # Define keyframes for entering, staying, and exiting
        enter_frame = 20
        start_stay_frame = 60  # Frame where the object finishes entering and starts its stay
        end_stay_frame = 90  # Frame where the object ends its stay and begins to exit
        exit_frame = 130  # Frame by which the object has exited

        # Animate the object with entering, staying, and exiting phases
        animated_obj = create_random_object()  # Create a random object
        animate_object(animated_obj, enter_location, stay_location, exit_location, enter_frame, start_stay_frame, end_stay_frame, exit_frame)

        # Setup camera to focus on the general area where action happens
        target_location = (0, 0, 1)
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = target_location 
        setup_camera(target)

        # Adjust scene's end frame to accommodate the last animation
        bpy.context.scene.frame_end = exit_frame + 30

        # Render the animation
        bpy.ops.render.render(animation=True)

        # Cleanup the target object after rendering
        bpy.data.objects.remove(target)


# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\departing"
generate_videos(base_path)
