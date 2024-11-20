import bpy
import random
import math 
from basic_setup_appearance import *

def create_random_object_set2():
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


    # Assuming 'create_glossy_mix_node_group' is already defined and called
    glossy_mix_group = create_glossy_mix_node_group()

    # Create a new material
    material = bpy.data.materials.new(name="GlossyMixMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # Clear any existing nodes
    nodes.clear()

    # Add a shader node group to use the custom node group
    group_node = nodes.new('ShaderNodeGroup')
    # Assign the node tree of the created group to this shader node group
    group_node.node_tree = glossy_mix_group

    # Connect the group output to the material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    links = material.node_tree.links
    links.new(group_node.outputs['Shader Output'], material_output.inputs['Surface'])

    obj = bpy.context.object


    # Assign the material to the object
    if obj.data.materials:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

    return obj, object_type

def setup_lights():

    add_point_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), radius=0.1, energy=0.45, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=0.45, angle_degrees=11.4, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=0.45, radius=0.1, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), shape='SQUARE', size=0.1, color=(1, 1, 1), energy=0.45, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)

    add_point_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), radius=1.0, energy=2, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=15, angle_degrees=10, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=2, radius=1.0, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), shape='SQUARE', size=1.0, color=(1, 1, 1), energy=2, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)
    
    add_point_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), color=(1, 1, 1), radius=0.5, energy=3, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), color=(1, 1, 1), energy=3, angle_degrees=53.1, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), color=(1, 1, 1), energy=3, radius=0.5, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), shape='SQUARE', size=0.5, color=(1, 1, 1), energy=3, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)

def setup_lights():

    add_point_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), radius=0.1, energy=0.45, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=0.45, angle_degrees=11.4, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=0.45, radius=0.1, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(11, -6, 25), rotation=(math.radians(-45), 0, 0), shape='SQUARE', size=0.1, color=(1, 1, 1), energy=0.45, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)

    add_point_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), radius=1.0, energy=2, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=15, angle_degrees=10, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), color=(1, 1, 1), energy=2, radius=1.0, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(-10, 3, 6), rotation=(math.radians(-45), 0, 0), shape='SQUARE', size=1.0, color=(1, 1, 1), energy=2, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)
    
    add_point_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), color=(1, 1, 1), radius=0.5, energy=3, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_sun_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), color=(1, 1, 1), energy=3, angle_degrees=53.1, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_spot_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), color=(1, 1, 1), energy=3, radius=0.5, spot_size_degrees=45, spot_blend=0.15, max_bounces=1024, cast_shadow=True, importance_sampling=True)
    add_area_light(location=(-5, -40, 3), rotation=(math.radians(-20), 0, 0), shape='SQUARE', size=0.5, color=(1, 1, 1), energy=3, max_bounces=1024, cast_shadow=True, importance_sampling=True, spread_degrees=180)

# Function to create a background image BSDF
def create_background_image(image_path):
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, -20, 0))
    background_plane = bpy.context.object
    background_plane.name = 'Background'
    background_plane.rotation_euler = (math.radians(90), 0, math.radians(180))
    
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
    angles = [75, 80, 90, 100, 105]
    
    # Randomly select one of the angles for the camera position
    angle = math.radians(random.choice(angles))
    
    # Define a radius for how far from the target the camera should be
    radius = 30
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(3, 10)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_object_right_path(obj, start_pos, end_pos, start_frame, end_frame):
    """Animate the object in a ']' shaped path."""
    mid_frame = (start_frame + end_frame) // 2

    # Start position
    obj.location = start_pos
    obj.keyframe_insert(data_path="location", frame=start_frame)

    # Mid position (move forward)
    mid_pos = (start_pos[0], end_pos[1], start_pos[2])
    obj.location = mid_pos
    obj.keyframe_insert(data_path="location", frame=mid_frame)

    # End position
    obj.location = end_pos
    obj.keyframe_insert(data_path="location", frame=end_frame)

def animate_object_left_path(obj, start_pos, end_pos, start_frame, end_frame):
    """Animate the object in a '[' shaped path."""
    mid_frame = (start_frame + end_frame) // 2

    # Start position
    obj.location = start_pos
    obj.keyframe_insert(data_path="location", frame=start_frame)

    # Mid position (move backward)
    mid_pos = (end_pos[0], start_pos[1], end_pos[2])
    obj.location = mid_pos
    obj.keyframe_insert(data_path="location", frame=mid_frame)

    # End position
    obj.location = end_pos
    obj.keyframe_insert(data_path="location", frame=end_frame)

    bpy.context.scene.frame_end = end_frame


# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\occlusion4_front_id_{i+1}.mp4"
        setup_scene(output_file_path)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        # Create two objects
        obj1, obj1_shape = create_random_object_set2()
        obj2, obj2_shape = create_random_object_set2()

        if obj1_shape == 'CONE' or obj1_shape == 'PYRAMID': # cone or pyramid is not big enough
            obj1.scale = (1.5, 1.5, 1.5)
        if obj2_shape == 'CONE' or obj2_shape == 'PYRAMID': # cone or pyramid is not big enough
            obj2.scale = (1.5, 1.5, 1.5)


        # Create two objects
        obj3, obj3_shape = create_random_object_set2()
        obj4, obj4_shape = create_random_object_set2()

        if obj3_shape == 'CONE' or obj3_shape == 'PYRAMID': # cone or pyramid is not big enough
            obj3.scale = (1.5, 1.5, 1.5)
        if obj4_shape == 'CONE' or obj4_shape == 'PYRAMID': # cone or pyramid is not big enough
            obj4.scale = (1.5, 1.5, 1.5)

        # Initial positions
        obj1.location = (6, -2, 1)  # Left side
        obj2.location = (6, 2, 1)   # Right side

        # Initial positions
        obj3.location = (-6, -2, 1)  # Left side
        obj4.location = (-6, 2, 1)   # Right side

        # Setup camera to focus on the center
        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = (0, 0, 1)
        setup_camera(target)

        # Define paths and animate
        start_frame = 1
        end_frame = 30
        animate_object_right_path(obj1, obj1.location, (8, -2, 1), start_frame, end_frame)  # Obj1 moves in ] shape
        animate_object_left_path(obj2, obj2.location, (4, 2, 1), start_frame, end_frame)  # Obj2 moves in [ shape
        animate_object_right_path(obj3, obj3.location, (-4, -2, 1), start_frame, end_frame)  # Obj1 moves in ] shape
        animate_object_left_path(obj4, obj4.location, (-8, 2, 1), start_frame, end_frame)  # Obj2 moves in [ shape

        start_frame = 31
        end_frame = 60
        animate_object_right_path(obj1, obj1.location, (8, 2, 1), start_frame, end_frame)  # Obj1 moves in ] shape
        animate_object_left_path(obj2, obj2.location, (4, -2, 1), start_frame, end_frame)  # Obj2 moves in [ shape
        animate_object_right_path(obj3, obj3.location, (-4, 2, 1), start_frame, end_frame)  # Obj1 moves in ] shape
        animate_object_left_path(obj4, obj4.location, (-8, -2, 1), start_frame, end_frame)  # Obj2 moves in [ shape

        start_frame = 61
        end_frame = 90
        animate_object_right_path(obj1, obj1.location, (6, 2, 1), start_frame, end_frame)  # Obj1 moves in ] shape
        animate_object_left_path(obj2, obj2.location, (6, -2, 1), start_frame, end_frame)  # Obj2 moves in [ shape
        animate_object_right_path(obj3, obj3.location, (-6, 2, 1), start_frame, end_frame)  # Obj1 moves in ] shape
        animate_object_left_path(obj4, obj4.location, (-6, -2, 1), start_frame, end_frame)  # Obj2 moves in [ shape

        bpy.ops.render.render(animation=True)


# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\occlusion"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)
