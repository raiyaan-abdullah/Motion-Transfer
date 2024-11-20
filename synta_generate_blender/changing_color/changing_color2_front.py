import bpy
import random
import math 
from basic_setup_appearance import *

# Function to create random object and apply glistening material
def create_random_object_basic_set1():
    objects = ['CUBE', 'CONE', 'PYRAMID', 'PRISM']
    object_type = random.choice(objects)

    # Add object to the scene based on random choice
    if object_type == 'CUBE':
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    elif object_type == 'CONE':
        bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, location=(0, 0, 1))
    elif object_type == 'PYRAMID':
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=1, depth=2, location=(0, 0, 1))
    elif object_type == 'PRISM':
        # Create a triangular prism (as an example)
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=2, location=(0, 0, 1))
        prism_obj = bpy.context.object

        # Optionally, adjust the prism to align one of the vertices with the world axis, or perform other transformations

        # Smooth the prism shape
        bpy.ops.object.shade_smooth()

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


# Function to animate a smooth color change of the material from one color to another over frames 1 to 20
def animate_color_change(obj, initial_color, final_color, start_frame, color_change_end_frame, total_end_frame):
    material = obj.data.materials[0]
    bsdf = material.node_tree.nodes.get('Principled BSDF')
    color_node = bsdf.inputs['Base Color']

    # Set initial color at the start frame
    color_node.default_value = initial_color
    color_node.keyframe_insert('default_value', frame=start_frame)
    
    # Change to final color by the color change end frame
    color_node.default_value = final_color
    color_node.keyframe_insert('default_value', frame=color_change_end_frame)
    
    # Ensure the color stays the same until the total end frame
    color_node.keyframe_insert('default_value', frame=total_end_frame)

def animate_swap_colors_between_objects(obj1, obj2, start_frame, swap_frame, total_end_frame):
    # Assuming obj1 and obj2 have materials with a Principled BSDF shader
    start_color1 = tuple(obj1.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value)
    start_color2 = tuple(obj2.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value)
    
    # Animate obj1 to change to obj2's color
    animate_color_change(obj1, start_color1, start_color2, start_frame, swap_frame, total_end_frame)
    
    # Animate obj2 to change to obj1's color
    animate_color_change(obj2, start_color2, start_color1, start_frame, swap_frame, total_end_frame)
    
    
    # No need to re-insert keyframes for the total end frame if the color should stay the same after swapping

            
# Main function to generate videos with adjusted parameters for the smooth color transition
def generate_videos(base_path, number_of_videos=50):
    images = ["castle.jpg", "coffee_shop.jpg", "city_sunset.jpg", "desert.jpg", "fire.jpg", "forest.jpg", "galaxy.jpg", "gym.jpg", "hospital.jpg", "hotel.jpg"]
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\changing_color2_front_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Create the first random object with a glistening material
        obj1 = create_random_object_basic_set1()
        # Immediately move obj1 to a new random location
        obj1.location = (-2, -3, 1)

        # Create the second random object with a glistening material
        obj2 = create_random_object_basic_set1()
        # Immediately move obj2 to a new random location, ensuring it's different from obj1's location
        obj2.location = (2, 3, 1)


        # Setup camera to focus on one of the objects or adjust for a general view
        avg_end_location = tuple(sum(coords)/3 for coords in zip(*[obj1.location, obj2.location]))
        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = avg_end_location
        setup_camera(target)

        # Define animation frames for color swap and overall animation duration
        start_frame = 1
        swap_frame = 90
        total_end_frame = 120

        # Swap colors between obj1 and obj2
        animate_swap_colors_between_objects(obj1, obj2, start_frame, swap_frame, total_end_frame)

        bpy.context.scene.frame_start = start_frame
        bpy.context.scene.frame_end = total_end_frame

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\changing_color"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)