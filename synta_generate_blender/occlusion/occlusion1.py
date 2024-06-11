import bpy
import random
import math 
from basic_setup import *

def create_random_object():
    objects = ['CUBE', 'SPHERE', 'CONE', 'CYLINDER', 'TORUS', 'ICO_SPHERE', 'PYRAMID', 'DODECAHEDRON', 'CAPSULE', 'PRISM']
    object_type = random.choice(objects)

    # Add object to the scene based on random choice
    if object_type == 'CUBE':
        bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    elif object_type == 'SPHERE':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
    elif object_type == 'CONE':
        bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, location=(0, 0, 1))
    elif object_type == 'CYLINDER':
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, location=(0, 0, 1))
    elif object_type == 'TORUS':
        bpy.ops.mesh.primitive_torus_add(location=(0, 0, 1))
    elif object_type == 'ICO_SPHERE':
        bpy.ops.mesh.primitive_ico_sphere_add(radius=1, location=(0, 0, 1))
    elif object_type == 'PYRAMID':
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=1, depth=2, location=(0, 0, 1))
    elif object_type == 'DODECAHEDRON':
        # Start with an icosphere; you might need to adjust subdivisions for your specific needs
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1, location=(0, 0, 1))
        obj = bpy.context.object

        # Add Decimate modifier to create a more polygonal shape
        bpy.ops.object.modifier_add(type='DECIMATE')
        dec_mod = obj.modifiers['Decimate']
        dec_mod.decimate_type = 'COLLAPSE'
        # The ratio determines the final amount of geometry; lower values mean more reduction
        dec_mod.ratio = 0.2  # Adjust this value as needed to get closer to a dodecahedron appearance

        # Apply the modifier to see the changes in the viewport
        bpy.ops.object.modifier_apply(modifier='Decimate')
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
    elif object_type == 'PRISM':
        # Create a triangular prism (as an example)
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, radius=1, depth=2, location=(0, 0, 1))
        prism_obj = bpy.context.object

        # Optionally, adjust the prism to align one of the vertices with the world axis, or perform other transformations

        # Smooth the prism shape
        bpy.ops.object.shade_smooth()


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

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))  # Adjust size as needed
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
    angles = [70, 75, 80, 90, 100, 105, 110]
    
    # Randomly select one of the angles for the camera position
    angle = math.radians(random.choice(angles))
    
    # Define a radius for how far from the target the camera should be
    radius = 22
    
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
def animate_moving_object(moving_obj):
    start_frame = 1
    end_frame = 60  # Adjust for speed of movement

    # Initial position is already set when the object was created
    moving_obj.keyframe_insert(data_path="location", frame=start_frame)
    
    # Ending position: move in front of the stationary object
    moving_obj.location.x = 0  # Center in front of the stationary object
    moving_obj.keyframe_insert(data_path="location", frame=end_frame)
    
    bpy.context.scene.frame_end = end_frame

# Main function to generate videos
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\occlusion1_id_{i+1}.mp4"  # Unique filename for each video
        setup_scene(output_file_path)

        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

        setup_lights()
        create_plane()

        # Create a random object with glistening material
        stationary_obj, stationary_shape = create_random_object()
        stationary_obj.location = (0, -1, 1)
        if stationary_shape == 'CONE' or stationary_shape == 'PYRAMID': # cone or pyramid is not big enough
            stationary_obj.scale = (3, 3, 3)
        else:
            stationary_obj.scale = (2, 2, 2)

        moving_obj, moving_shape = create_random_object()
        moving_obj.location = (-5, 3, 1)


        # Setup camera to focus on the object
        target = bpy.data.objects.new("Target", None)
        bpy.context.collection.objects.link(target)
        target.location = (0,0,1)
        setup_camera(target)

        # Animate the moving object
        animate_moving_object(moving_obj)

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\occlusion"
generate_videos(base_path)
