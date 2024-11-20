import bpy
import random
import math 
from basic_setup_appearance import *

# Function to create random object and apply glistening material
def create_random_object_basic_set2():
    objects = ['SPHERE', 'CYLINDER', 'TORUS', 'CAPSULE']
    object_type = random.choice(objects)

    # Add object to the scene based on random choice
    if object_type == 'SPHERE':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
    elif object_type == 'CYLINDER':
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 1))
    elif object_type == 'TORUS':
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, 1))
    elif object_type == 'CAPSULE':
        # Create cylinder
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 1))
        cylinder = bpy.context.object
        
        # Create top sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 2))
        top_sphere = bpy.context.object
        
        # Create bottom sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        bottom_sphere = bpy.context.object

        # Select all parts of the capsule
        bpy.ops.object.select_all(action='DESELECT')
        cylinder.select_set(True)
        top_sphere.select_set(True)
        bottom_sphere.select_set(True)
        bpy.context.view_layer.objects.active = cylinder

        # Join the parts into a single object
        bpy.ops.object.join()

    obj = bpy.context.object

    # Apply a glistening material with specific metallic and roughness properties
    material = bpy.data.materials.new(name="GlisteningMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = random_color()  # Random color
    bsdf.inputs['Metallic'].default_value = 0.9  # High metallic value
    bsdf.inputs['Roughness'].default_value = 0.6  # Low roughness value for glisten
    obj.data.materials.append(material)

    return obj

def create_background_image(image_path):
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
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
    radius = 12
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(5, 15)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)


def animate_smooth_color_change(obj, start_frame, mid_frame, return_to_initial_frame):
    material = obj.data.materials[0]
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    color_node = bsdf.inputs['Base Color']

    initial_color = tuple(color_node.default_value)  # Save the initial color
    new_color = (random.random(), random.random(), random.random(), 1)  # Generate a new random color

    # Set the color to initial at the start frame
    color_node.default_value = initial_color
    color_node.keyframe_insert('default_value', frame=start_frame)

    # Change to the new color by the mid frame
    color_node.default_value = new_color
    color_node.keyframe_insert('default_value', frame=mid_frame)

    # Change back to the initial color by the return_to_initial_frame
    color_node.default_value = initial_color
    color_node.keyframe_insert('default_value', frame=return_to_initial_frame)

    # Ensure the animation system updates the material changes
    bpy.context.view_layer.update()
            
# Main function to generate videos with adjusted parameters for the smooth color transition
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\changing_color5_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Create a random object with glistening material
        obj = create_random_object_basic_set2()

        # Setup camera to focus on the object
        setup_camera(obj)

        # Define frames for color change and staying
        start_frame = 1
        mid_frame = 60  # Frame at which color changes to new color
        stay_with_new_color_frame = mid_frame + 20  # Stay with new color for 20 frames
        return_to_initial_frame = stay_with_new_color_frame + 20  # Return to initial color 20 frames after new color
        stay_in_initial_color_frame = return_to_initial_frame + 30  # Stay in initial color for 30 frames after returning
        
        # Animate smooth color change
        animate_smooth_color_change(obj, start_frame, mid_frame, return_to_initial_frame)
        
        bpy.context.scene.frame_start = start_frame
        bpy.context.scene.frame_end = stay_in_initial_color_frame  # Extend to stay with final color for 30 frames

        # Render the animation
        bpy.ops.render.render(animation=True)


# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\changing_color"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
