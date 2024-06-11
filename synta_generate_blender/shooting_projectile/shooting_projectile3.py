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
    z = random.uniform(15, 35)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_projectile_trajectory(obj, start_location, initial_velocity, launch_angle_degrees, gravity=-9.81, frame_rate=24):
    """
    Animate the trajectory of a projectile in Blender.

    Args:
    - obj: bpy.types.Object - The object to animate.
    - start_location: tuple - The initial location of the projectile (x, y, z).
    - initial_velocity: float - The initial velocity of the projectile.
    - launch_angle_degrees: float - The launch angle in degrees.
    - gravity: float - Acceleration due to gravity (m/s^2). Default is -9.81 m/s^2.
    - frame_rate: int - Frame rate of the animation. Default is 24 frames per second.

    Returns:
    - None
    """
    # Convert angle to radians
    launch_angle_radians = math.radians(launch_angle_degrees)

    # Calculate initial velocity components
    initial_velocity_x = initial_velocity * math.cos(launch_angle_radians)
    initial_velocity_y = initial_velocity * math.sin(launch_angle_radians)

    # Calculate time increment
    delta_time = 1 / frame_rate

    # Set initial frame
    bpy.context.scene.frame_set(0)

    # Set initial position keyframe
    obj.location = start_location
    obj.keyframe_insert(data_path="location")

    # Animate trajectory
    time = 0
    while obj.location[2] >= start_location[2]:
        x = start_location[0] + initial_velocity_x * time
        y = start_location[1] + initial_velocity_y * time
        z = start_location[2] - (initial_velocity_x * time) + (0.5 * gravity * (time ** 2))
        obj.location = (x, y, z)
        obj.keyframe_insert(data_path="location", frame=int(time * frame_rate))
        time += delta_time

    # Final keyframe
    obj.location = (x, y, start_location[2])
    obj.keyframe_insert(data_path="location", frame=int(time * frame_rate))




# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\shooting3_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create a random object with glistening material
        obj1 = create_random_object()


        # Setup camera to focus on the falling object
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = obj1.location  # Focus on the object
        setup_camera(target)

        
        # Assuming you have created a random object named obj1 and want it to rise from start location (5, 5, 1) to peak height and stay there
        animate_projectile_trajectory(obj1, start_location=(7, 7, 1), initial_velocity= 8, launch_angle_degrees= 180)


        # Render the animation
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\shooting_projectile"
generate_videos(base_path)

