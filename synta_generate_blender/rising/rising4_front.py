import bpy
import random
import math 
from basic_setup_appearance import *

# Function to create a background image BSDF
def create_background_image(image_path):
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 20, 0))
    background_plane = bpy.context.object
    background_plane.name = 'Background'
    background_plane.rotation_euler = (math.radians(90), 0, 0)
    
    material = bpy.data.materials.new(name="BackgroundMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Roughness'].default_value = 1.0
    
    
    tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(image_path)
    
    emission_node = material.node_tree.nodes.new('ShaderNodeEmission')
    emission_node.inputs['Strength'].default_value = 2.0  # Adjust this value to control brightness
    
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
    
    background_plane.data.materials.append(material)

def setup_camera(target):
    # Define 6 distinct angles around the target, in radians
    angles = [75, 80, 85, 90, 95, 100, 105]
    
    # Randomly select one of the angles for the camera position
    angle = math.radians(random.choice(angles))
    
    # Define a radius for how far from the target the camera should be
    radius = 30
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = -(radius * math.sin(angle) + target.location.y)
    z = random.uniform(5, 10)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_projectile_trajectory(obj, start_location, initial_velocity, launch_angle_degrees, gravity=-9.81, frame_rate=24, end_frame = 70):
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
    frame = int(time * frame_rate)
    prev_z = 0
    while obj.location[2] >= start_location[2] and frame<=end_frame:
        x = start_location[0] + initial_velocity_x * time
        y = start_location[1]
        z = start_location[2] + (initial_velocity_y * time) + (0.5 * gravity * (time ** 2))
        if z>prev_z:
            prev_z = z
            obj.location = (x, y, z)
        else:
            obj.location = (x, y, prev_z)
        obj.keyframe_insert(data_path="location", frame= frame)
        time += delta_time
        frame = int(time * frame_rate)

    # Final keyframe
    obj.location = (x, y, start_location[2])
    obj.keyframe_insert(data_path="location", frame=frame)
    bpy.context.scene.frame_end = end_frame




# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\rising4_front_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Create a random object with glistening material
        obj1 = create_random_object_set2()


        # Setup camera to focus on the falling object
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = obj1.location  # Focus on the object
        setup_camera(target)

        
        # Assuming you have created a random object named obj1 and want it to rise from start location (5, 5, 1) to peak height and stay there
        animate_projectile_trajectory(obj1, start_location=(-6, -6, 1), initial_velocity= 11.5, launch_angle_degrees= 60, end_frame = 70)

        
        # Render the animation
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\rising"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

