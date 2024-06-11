import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=25, location=(0, 0, 0))  # Adjust size as needed
    ground_plane = bpy.context.object
    ground_plane.name = 'Ground'
    # Optional: Adjust the ground material
    if not bpy.data.materials.get("GroundMaterial"):
        ground_material = bpy.data.materials.new(name="GroundMaterial")
    else:
        ground_material = bpy.data.materials["GroundMaterial"]
    ground_material.diffuse_color = (0.8, 0.8, 0.8, 1)  # Light grey color
    if ground_plane.data.materials:
        ground_plane.data.materials[0] = ground_material
    else:
        ground_plane.data.materials.append(ground_material)

def setup_camera(target):
    # Define 6 distinct angles around the target, in radians
    angles = [0, math.pi / 3, 2 * math.pi / 3, math.pi, 4 * math.pi / 3, 5 * math.pi / 3]
    
    # Randomly select one of the angles for the camera position
    angle = random.choice(angles)
    
    # Define a radius for how far from the target the camera should be
    radius = 50
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(15, 40)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

# Animate the object moving into view
def animate_leader_with_followers_in_line(leader, followers, start_frame, end_frame, leader_start_location, leader_end_location):
    """
    Animates a leader object to move in a straight line with multiple followers maintaining a constant offset from each other.
    
    Parameters:
    - leader: The leading object to animate.
    - followers: A list of following objects to animate.
    - start_frame: The frame at which the animation starts.
    - end_frame: The frame at which the animation ends.
    - leader_start_location: The starting location of the leader as a tuple (x, y, z).
    - leader_end_location: The ending location of the leader as a tuple (x, y, z).
    """
    fps = bpy.context.scene.render.fps  # Frames per second
    total_frames = end_frame - start_frame
    leader_movement_vector = tuple(leader_end_location[i] - leader_start_location[i] for i in range(3))
    
    for frame in range(start_frame, end_frame + 1):
        fraction_of_journey = (frame - start_frame) / total_frames
        leader_new_location = tuple(leader_start_location[i] + fraction_of_journey * leader_movement_vector[i] for i in range(3))
        
        # Update and keyframe leader location
        leader.location = leader_new_location
        leader.keyframe_insert(data_path="location", frame=frame)

        for idx, follower in enumerate(followers):
            follower_offset = (3 * (idx + 1), 0, 0)  # Increase the X offset for each follower
            follower_new_location = tuple(leader_new_location[i] - follower_offset[i] for i in range(3))
            
            # Update and keyframe follower location
            follower.location = follower_new_location
            follower.keyframe_insert(data_path="location", frame=frame)





# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\following3_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create leader and follower objects using the function
        leader = create_random_object()
        
        # Create multiple followers
        num_followers = 3  # For example, 3 followers
        followers = [create_random_object() for _ in range(num_followers)]
        # Define animation parameters
        start_frame = 1
        end_frame = 120
        leader_start_location = (-1, 0, 1)  # Assuming a height of 5 units
        leader_end_location = (12, 0, 1)  # Moves 10 units along the X-axis

        # Ensure the leader and followers are at their starting positions
        leader.location = leader_start_location
        for idx, follower in enumerate(followers):
            follower_offset = (3 * (idx + 1), 0, 0)
            follower.location = (leader_start_location[0] - follower_offset[0], leader_start_location[1], leader_start_location[2])

        # Setup camera to focus on the leader object
        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = leader.location
        setup_camera(target)
    
        # Animate the leader with followers
        animate_leader_with_followers_in_line(leader, followers, start_frame, end_frame, leader_start_location, leader_end_location)


        # Render the animation
        bpy.ops.render.render(animation=True)



# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\following"
generate_videos(base_path)

