import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=35, location=(0, 0, 0))  # Adjust size as needed
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
    radius = 28
    
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
def animate_bouncing(obj, start_frame, end_frame, start_height, floor_level=0, bounces=3):
    """
    Animates an object with a simplified bouncing effect.
    
    Parameters:
    - obj: The object to animate.
    - start_frame: The frame at which the animation starts.
    - end_frame: The frame at which the animation ends.
    - start_height: The starting height of the object above the floor.
    - floor_level: The Z-level at which the object bounces.
    - bounces: The number of times the object bounces before coming to rest.
    """
    scene = bpy.context.scene
    
    frames_per_bounce = int((end_frame - start_frame) / bounces)
    current_frame = start_frame
    height = start_height
    
    for bounce in range(bounces):
        # Peak of the bounce
        obj.location.z = height + floor_level
        obj.keyframe_insert(data_path="location", frame=current_frame)
        
        # Falling to the floor level
        next_keyframe = current_frame + frames_per_bounce // 2
        obj.location.z = floor_level
        obj.keyframe_insert(data_path="location", frame=next_keyframe)
        
        # Reduce height for the next bounce
        height /= 2
        current_frame += frames_per_bounce
    
    # Ensure the object ends at the floor level
    obj.location.z = floor_level
    obj.keyframe_insert(data_path="location", frame=end_frame)

# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\bouncing2_id_{i + 1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Parameters for the bouncing objects
        start_heights = [4, 5, 3, 6]  # Varied start heights for visual interest
        floor_level = 1  # Common floor level for all objects
        bounces = 4  # Number of bounces
        start_positions = [(0, -6, 1), (0, -2, 1), (0, 2, 1), (0, 6, 1)]  # Starting positions for each object

        target = bpy.data.objects.new("Target", None)  # Create an empty object to serve as a target
        bpy.context.collection.objects.link(target)
        target.location = (0, 0, 0)
        setup_camera(target)

        # Create and animate each object
        for i, start_position in enumerate(start_positions):
            obj = create_random_object()
            obj.location = start_position  # Set initial location
            
            # Adjust the Z coordinate to the start height for bouncing
            obj.location.z += start_heights[i] - floor_level
            
            
            # Animate the object bouncing
            animate_bouncing(obj, start_frame=1, end_frame=120, start_height=start_heights[i], floor_level=floor_level, bounces=bounces)

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\bouncing"
generate_videos(base_path)
