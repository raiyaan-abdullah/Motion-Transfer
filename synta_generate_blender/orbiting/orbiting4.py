import bpy
import random
import math 
from basic_setup_appearance import *

def create_background_image(image_path):
    bpy.ops.mesh.primitive_plane_add(size=25, location=(0, 0, 0))
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
    radius = 25
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(15, 30)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_orbit1(obj, center, start_frame, end_frame, clockwise=True):
    
    radius = 5
    num_frames = end_frame - start_frame + 1
    for frame in range(num_frames):
        angle = 2 * math.pi * (frame / num_frames)
        if clockwise:
            x = center.location.x + radius * math.cos(angle)
            y = center.location.y - radius * math.sin(angle)
        else:
            x = center.location.x + radius * math.cos(angle)
            y = center.location.y + radius * math.sin(angle)
        obj.location = (x, y, center.location.z)
        obj.keyframe_insert(data_path="location", frame=start_frame + frame)

def animate_orbit2(obj, center, start_frame, end_frame, clockwise=True):
    
    radius = 5
    num_frames = end_frame - start_frame + 1
    for frame in range(num_frames):
        angle = 2 * math.pi * (frame / num_frames)
        if clockwise:
            x = center.location.x - radius * math.cos(angle)
            y = center.location.y - radius * math.sin(angle)
        else:
            x = center.location.x + radius * math.cos(angle)
            y = center.location.y + radius * math.sin(angle)
        obj.location = (x, y, center.location.z)
        obj.keyframe_insert(data_path="location", frame=start_frame + frame)
        print(x," ",y)
                


def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\orbiting4_id_{i+1}.mp4"  # Adjust path as necessary

        # Setup scene for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        obj1 = create_random_object_set2()
        obj2 = create_random_object_set2()  # Start offset from obj1
        
        obj1.location = (-3, 0, 1)
        obj2.location = (2, 0, 1)

        # Setup camera to focus on the general area where action happens
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = (0, 0, 1)  # Focus on the center of the action
        setup_camera(target)

        # Animate obj2 orbiting obj1
        animate_orbit1(obj2, obj1, start_frame=1, end_frame=80, clockwise=True)

        animate_orbit2(obj1, obj2, start_frame=81, end_frame=160, clockwise=True)


        # Set scene end frame
        bpy.context.scene.frame_end = 180

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\orbiting"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
