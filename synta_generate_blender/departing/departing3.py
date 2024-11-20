import bpy
import random
import math 
from basic_setup_appearance import *

def create_background_image(image_path):
    bpy.ops.mesh.primitive_plane_add(size=35, location=(0, 0, 0))
    background_plane = bpy.context.object
    background_plane.name = 'Background'
    
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
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\departing3_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Define start locations further from the center
        start_locations = [
            (-3, -3, 1),   # Increased separation
            (3, -3, 1),  # Increased separation
            (0, 3, 1)    # Increased separation
        ]
        # Define distinct end locations further apart
        end_locations = [
            (-30, -30, 1),  # Increased separation
            (30, -30, 1),   # Increased separation
            (0, -30, 1)     # Increased separation
        ]

        # Animation frame settings
        animation_length = 60
        frame_offset = 20  # Number of frames to wait before starting the next object's animation

        # Create, animate three objects with staggered start times
        current_start_frame = 1
        for start_location, end_location in zip(start_locations, end_locations):
            obj = create_random_object_set2()  # Create a random object
            # Animate object with staggered frames
            animate_object(obj, start_location, end_location, current_start_frame, current_start_frame + animation_length)
            current_start_frame += animation_length + frame_offset

        # Setup camera to focus on a general area where action happens
        avg_end_location = (0,0,1)
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = avg_end_location
        setup_camera(target)

        # Adjust scene's end frame to accommodate the last animation
        bpy.context.scene.frame_end = current_start_frame + animation_length

        # Render the animation
        bpy.ops.render.render(animation=True)

        # Cleanup the target object after rendering
        bpy.data.objects.remove(target)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\departing"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
