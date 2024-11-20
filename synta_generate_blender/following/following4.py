import bpy
import random
import math 
from basic_setup_appearance import *

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
    radius = 40
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(15, 35)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_objects_along_path(leader, follower, start_frame, end_frame, path_points, follower_offset):
    fps = bpy.context.scene.render.fps
    total_frames = end_frame - start_frame
    path_segments = len(path_points) - 1
    frames_per_segment = total_frames // path_segments
    
    for i, point in enumerate(path_points[:-1]):
        next_point = path_points[i + 1]
        for frame in range(frames_per_segment):
            fraction_of_segment = frame / frames_per_segment
            leader_new_location = (
                point[0] + fraction_of_segment * (next_point[0] - point[0]),
                point[1] + fraction_of_segment * (next_point[1] - point[1]),
                point[2] + fraction_of_segment * (next_point[2] - point[2])
            )
            follower_new_location = tuple(leader_new_location[i] - follower_offset[i] for i in range(3))
            current_frame = start_frame + i * frames_per_segment + frame
            leader.location = leader_new_location
            leader.keyframe_insert(data_path="location", frame=current_frame)
            follower.location = follower_new_location
            follower.keyframe_insert(data_path="location", frame=current_frame)

def generate_zigzag_path(start_location, end_location, num_points, zigzag_intensity=5):
    path_points = [start_location]
    for i in range(1, num_points - 1):
        if i % 2 == 0:
            # Move in x direction
            x = random.uniform(-zigzag_intensity, zigzag_intensity) + path_points[-1][0]
            y = path_points[-1][1]
        else:
            # Move in y direction
            x = path_points[-1][0]
            y = random.uniform(-zigzag_intensity, zigzag_intensity) + path_points[-1][1]
        z = random.uniform(start_location[2], end_location[2])  # Optional variation in z
        path_points.append((x, y, z))
    path_points.append(end_location)
    return path_points

def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\following4_id_{i+1}.mp4"
        setup_scene(output_file_path)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_background_image(image_path+images[i%10])

        obj1 = create_random_object_set2()
        obj2 = create_random_object_set2()

        start_frame = 1
        end_frame = 120
        leader_start_location = (0, 0, 1)
        leader_end_location = (10, 10, 1)
        follower_offset = (3, 0, 0)

        obj1.location = leader_start_location
        obj2.location = (leader_start_location[0] - follower_offset[0], leader_start_location[1] - follower_offset[1], leader_start_location[2] - follower_offset[2])

        zigzag_path = generate_zigzag_path(leader_start_location, leader_end_location, num_points=10, zigzag_intensity=5)  # Adjust num_points and zigzag_intensity as needed

        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = obj1.location
        setup_camera(target)

        animate_objects_along_path(obj1, obj2, start_frame, end_frame, zigzag_path, follower_offset)

        bpy.context.scene.frame_end = end_frame

        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\following"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

