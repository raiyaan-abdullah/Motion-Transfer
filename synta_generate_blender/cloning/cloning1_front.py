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
    clone2.location.y += 10  # Move the other clone down
    clone1.keyframe_insert(data_path="location", frame=end_frame)
    clone2.keyframe_insert(data_path="location", frame=end_frame)
    bpy.context.scene.frame_end = end_frame + 20

# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\cloning1_front_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Create a random object with glistening material
        obj = create_random_object_set1()

        # Setup camera to focus on the object
        obj_location = obj.location
        end_locations = [
            obj_location,
            (obj_location.x, obj_location.y + 4, obj_location.z),
            (obj_location.x, obj_location.y + 10, obj_location.z)
        ]
        avg_end_location = tuple(sum(coords)/3 for coords in zip(*end_locations))
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = avg_end_location
        setup_camera(target)

        # Add animation, camera, and lighting setup here (omitted for brevity)
        animate_object(obj)

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\cloning"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
