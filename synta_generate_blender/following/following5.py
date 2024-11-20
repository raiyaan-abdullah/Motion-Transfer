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
    radius = 35
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(20, 35)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_meeting_and_following(leader, follower, start_frame, end_frame, leader_start_location, follower_start_location, meeting_x_difference):
    fps = bpy.context.scene.render.fps
    total_frames = end_frame - start_frame
    leader_speed_x = 0.2  # Adjust as needed
    follower_speed_y = 0.15  # Adjust as needed

    for frame in range(start_frame, end_frame + 1):
        leader.location.x = leader_start_location[0] + leader_speed_x * (frame - start_frame)
        if follower.location.x > leader.location.x - 3:   
            follower.location.y = follower_start_location[1] + follower_speed_y * (frame - start_frame)
        else:
            follower.location.x = leader.location.x - meeting_x_difference

        leader.keyframe_insert(data_path="location", frame=frame)
        follower.keyframe_insert(data_path="location", frame=frame)


# Main function to generate videos
def generate_videos(base_path, number_of_videos=50):
    images = ["inside_white_house.jpg", "kitchen.jpg", "library.jpg", "ocean.jpg", "office.jpg", "rainy_farm.jpg", "sky_clouds.jpg", "storm.jpg", "underwater.jpg", "warehouse.jpg"]
    for i in range(number_of_videos):
        output_file_path = f"{base_path}\\following5_id_{i+1}.mp4"
        setup_scene(output_file_path)

        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()  # Ensure this function is defined elsewhere in your script
        create_background_image(image_path+images[i%10])

        leader = create_random_object_set2()
        follower = create_random_object_set2()

        start_frame = 1
        end_frame = 120  # Adjust as necessary
        leader_start_location = (-10, 0, 1)
        follower_start_location = (0, -13, 1)
        meeting_x_difference = 3

        leader.location = leader_start_location
        follower.location = follower_start_location

        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = (0,0,0)
        setup_camera(target)

        animate_meeting_and_following(leader, follower, start_frame, end_frame, leader_start_location, follower_start_location, meeting_x_difference)
        bpy.context.scene.frame_end = end_frame
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\following"
image_path = "C:\\synta_generate_blender\\backgrounds\\"
generate_videos(base_path)

