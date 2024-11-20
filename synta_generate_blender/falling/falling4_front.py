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
    radius = 40
    
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
def animate_parabolic_fall(obj, start_location, end_frame, gravity=-9.8, initial_velocity=(1, 0, 0)):
    """
    Animates an object falling in a parabolic trajectory.

    Parameters:
    - obj: The object to animate.
    - start_location: A tuple (x, y, z) representing the starting location.
    - end_frame: The frame at which the animation ends.
    - gravity: The gravitational acceleration (negative value).
    - initial_velocity: A tuple (vx, vy, vz) representing the initial velocity in each direction.
    """
    start_frame = 1
    fps = bpy.context.scene.render.fps  # Frames per second
    time_increment = 1 / fps
    total_time = end_frame / fps

    # Set the object's initial location
    obj.location = start_location
    obj.keyframe_insert(data_path="location", frame=start_frame)
    
    for frame in range(start_frame + 1, end_frame + 1):
        time = (frame - start_frame) * time_increment
        x = start_location[0] + initial_velocity[0] * time
        y = start_location[1] + initial_velocity[1] * time
        z = start_location[2] + initial_velocity[2] * time + 0.5 * gravity * time ** 2
        
        if z<0.5: #finish before object goes under plane
            break

        # Update object location
        obj.location = (x, y, z)
        obj.keyframe_insert(data_path="location", frame=frame)

    # Optionally, adjust the scene's end frame
    bpy.context.scene.frame_end = end_frame



# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\falling4_front_id_{i+1}.mp4"  # Unique filename for each video
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

        # Define the
    
        # Animate the object
        animate_parabolic_fall(obj1, start_location = (-8, -8, 8), end_frame=60, gravity=-9.8, initial_velocity = (5, 6, 1))

        # Render the animation
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\falling"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

