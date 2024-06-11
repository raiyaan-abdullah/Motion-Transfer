import bpy
import random
import math 
from basic_setup import *

# Function to create random object and apply glistening material
def create_random_object_basic():
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

def create_plane():
    # GROUND PLANE
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))  # Adjust size as needed
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

# Animate the object moving into view
def animate_fade_out(obj, start_frame, end_frame):
    # Ensure the object has a material
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="SimpleFadeMaterial")
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
def generate_videos(base_path, number_of_videos=100):
    for i in range(number_of_videos):
        # Setup scene for each video
        output_file_path = f"{base_path}\\disappearing1_id_{i+1}.mp4"  # Unique filename for each video
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

        create_plane()

        # Create a random object with glistening material
        obj = create_random_object_basic()

        # Setup camera to focus on the object
        setup_camera(obj)

        # Add animation, camera, and lighting setup here (omitted for brevity)
        animate_fade_out(obj, start_frame=1, end_frame=120)

        # Render the animation
        bpy.ops.render.render(animation=True)

# Assuming Windows path, adjust as needed
base_path = "C:\\synta\\disappearing"
generate_videos(base_path)
