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
def animate_fade_out(obj, start_frame, end_frame):

    # Ensure the object has a material
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="FadeMaterial")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]
    
    # Ensure using nodes and get nodes and links
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get('Principled BSDF') or nodes.new(type='ShaderNodeBsdfPrincipled')

    # Enable alpha blending for transparency to work in Eevee
    mat.use_backface_culling = True
    mat.blend_method = 'BLEND'

    # Animate alpha value of the Principled BSDF shader from 1 to 0
    bsdf.inputs['Alpha'].default_value = 1.0  # Fully opaque
    bsdf.inputs['Alpha'].keyframe_insert('default_value', frame=start_frame)
    bsdf.inputs['Alpha'].default_value = 0.0  # Fully transparent
    bsdf.inputs['Alpha'].keyframe_insert('default_value', frame=end_frame)


# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    # Define target locations for the objects
    locations = [(5, 0, 1), (-5, 0, 1), (0, 5, 1), (0, -5, 1)]

    animation_length = 30  # Length of each object's fade animation
    delay_between_fades = 10  # Delay between start of fade animations for consecutive objects
    
    
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}/disappearing3_id_{i+1}.mp4"
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        for obj in bpy.data.objects:
            # Check if the object is a light
            if obj.type == 'LIGHT':
                # Access the light's data block
                light = obj.data
                
                # Disable shadows
                light.use_shadow = False
                # If using Cycles renderer, you might need to set this as well
                light.cycles.cast_shadow = False

        create_background_image(image_path+images[i%10])

        # Calculate the total number of frames needed
        total_animation_frames = animation_length + (len(locations) - 1) * (animation_length + delay_between_fades)
        bpy.context.scene.frame_end = total_animation_frames

        start_frame = 1
        
        # Create 4 random objects at specific locations and animate them
        for location_index, location in enumerate(locations):
            obj = create_random_object_basic_set2()
            # Set each object's location
            obj.location = location

            # Calculate end frame for the current object's fade animation
            end_frame = start_frame + animation_length
            
            # Apply the fade-out animation to the current object
            animate_fade_out(obj, start_frame, end_frame)

            # Update start_frame for the next object
            start_frame += animation_length + delay_between_fades

        # Adjust camera setup if necessary to ensure it captures all objects appropriately
        # Setup camera to focus on the central action area
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = (0, 0, 1)  # Focus on the center of action
        setup_camera(target)

        # Render the animation
        bpy.ops.render.render(animation=True)


# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\disappearing"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
