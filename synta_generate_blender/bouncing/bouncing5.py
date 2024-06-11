import bpy
import random
import math 
from basic_setup import *

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))  # Adjust size as needed
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
    radius = 32
    
    # Calculate the camera's location using spherical coordinates
    x = radius * math.cos(angle) + target.location.x
    y = radius * math.sin(angle) + target.location.y
    z = random.uniform(25, 40)  # Adjust the Z to change the height of the camera
    
    # Add the camera at the calculated location
    bpy.ops.object.camera_add(location=(x, y, z))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    
    # Point the camera at the target object
    look_at(camera, target)

def create_stairs(name, step_count=10, step_size=(5, 2, 1)):
    """
    Creates a straight staircase model.

    Parameters:
    - name: Name of the staircase object.
    - step_count: Number of steps in the staircase.
    - step_size: Size of each step as a tuple (length, width, height).
    """
    bpy.ops.object.select_all(action='DESELECT')

    # Initial position of the first step at the base
    position = [0, 0, 0]

    for i in range(step_count):
        bpy.ops.mesh.primitive_cube_add(size=3, location=(position[0], position[1], position[2]))
        step = bpy.context.object
        # Adjust scale based on the desired step size (considering the cube's default size of 2)
        step.scale = (step_size[0] / 2, step_size[1] / 2, step_size[2] / 2)
        step.name = f"{name}_step_{i}"

        # Update position for the next step to be directly above the previous step
        position[1] += step_size[1]  # Increase height for the next step
        position[2] += step_size[2]  # Increase height for the next step

    # Optionally, join all steps into a single object for easier manipulation
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=f"{name}_step*")
    bpy.ops.object.join()
    stairs = bpy.context.object
    stairs.name = name

    # Create and assign highly reflective steel material
    steel_material = bpy.data.materials.new(name="ReflectiveSteelMaterial")
    steel_material.use_nodes = True
    bsdf = steel_material.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1)  # Light grey color, typical of steel
    bsdf.inputs['Metallic'].default_value = 1.0  # Full metallic effect for maximum reflectivity
    bsdf.inputs['Roughness'].default_value = 0.05  # Very low roughness for a glossy surface
    bsdf.inputs['Specular IOR Level'].default_value = 0.8  # High specular for strong light reflection


    # Assign material to stairs
    if stairs.data.materials:
        stairs.data.materials[0] = steel_material
    else:
        stairs.data.materials.append(steel_material)

def animate_bounce_series(obj, start_pos, num_bounces, y_increase, z_bounce_height, start_frame, frames_per_bounce):
    """
    Animate an object to bounce multiple times with increasing distance and a bouncing effect in z.

    Parameters:
    - obj: The object to animate.
    - start_pos: Starting position of the object (tuple of x, y, z).
    - num_bounces: Number of bounces.
    - y_increase: Increase in y for each bounce (moving forward).
    - z_bounce_height: Maximum height of each bounce in the z-direction.
    - start_frame: Animation start frame.
    - frames_per_bounce: Number of frames allocated per bounce.
    """
    
    obj.animation_data_clear()
    
    current_pos = list(start_pos)
    current_frame = start_frame
    
    for bounce in range(num_bounces):
        # Position at the start of the bounce
        obj.location = current_pos
        obj.keyframe_insert(data_path="location", frame=current_frame)
        
        # Peak of the bounce
        peak_frame = current_frame + frames_per_bounce // 2
        peak_pos = (current_pos[0], current_pos[1] + y_increase / 2, current_pos[2] + z_bounce_height)
        obj.location = peak_pos
        obj.keyframe_insert(data_path="location", frame=peak_frame)
        
        # End of the bounce, returning to original z but moving forward in y
        current_frame += frames_per_bounce
        current_pos[1] += y_increase  # Constantly moving forward
        current_pos[2] = start_pos[2]  # Return to original z height
        obj.location = current_pos
        obj.keyframe_insert(data_path="location", frame=current_frame)

    bpy.context.scene.frame_end = current_frame


# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\bouncing5_id_{i + 1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Assume stairs start at (0, 0, 5) and end at (10, 0, 0) with 10 steps
        stairs_start = (0, 0, 5)
        stairs_end = (10, 0, 0)
        step_count = 10
        
        # Create stairs
        #create_stairs(name="MyStairs", step_count=10)

        # Create a random object with glistening material
        obj = create_random_object()
        start_pos = (0, -1, 1)
        num_bounces = 9
        y_decrease = 2
        z_bounce_height = 2
        start_frame = 1
        frames_per_bounce = 10  # Adjust this for the timing of the bounces

        # Setup camera to focus on the object
        setup_camera(obj)

        # Animate the object bouncing
        animate_bounce_series(obj, start_pos, num_bounces, y_decrease, z_bounce_height, start_frame, frames_per_bounce)

        bpy.context.scene.frame_end = 100
        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\bouncing"
generate_videos(base_path)
