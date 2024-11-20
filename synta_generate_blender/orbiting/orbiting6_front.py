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
    radius = 35
    
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

def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\orbiting6_front_id_{i+1}.mp4"

        setup_scene(output_file_path)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        central_obj = create_random_object_set2()
        central_obj.location = (0, 0, 6)  # Elevated central object
        orbiting_obj = create_random_object_set2()
        orbiting_obj.location = (0, 0, 1)

        setup_camera(central_obj)
        animate_object(orbiting_obj, central_obj)
        bpy.ops.render.render(animation=True)


# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\orbiting"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
