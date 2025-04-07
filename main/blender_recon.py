import bpy
import json
import os
import numpy as np

# Define paths
FRAGMENT_FOLDER = "/home/kira/Desktop/healing_stones/aligned"  # Adjust this if needed
ALIGNMENT_PATH = "aligned_matches.json"
OUTPUT_PATH = "/home/kira/Desktop/reconstructed_model.ply"  # Change this to your desired output path

def load_fragment(filename):
    """Load the fragment PLY file into Blender."""
    filepath = os.path.join(FRAGMENT_FOLDER, f"{filename}.ply")
    bpy.ops.import_mesh.ply(filepath=filepath)
    return bpy.context.selected_objects[0]  # Return the imported object    

def apply_transformation(obj, transformation_matrix):
    """Apply a transformation matrix to a Blender object."""
    matrix = np.array(transformation_matrix)
    obj.matrix_world = matrix

def main():
    # Clear existing objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Load transformations from aligned matches
    with open(ALIGNMENT_PATH, 'r') as f:
        aligned_matches = json.load(f)

    # Create an empty list to hold all loaded fragments
    loaded_fragments = []

    # Import and transform fragments based on the saved alignments
    for match in aligned_matches:
        source = match["fragment_A"]
        target = match["fragment_B"]
        transformation = match["transformation"]

        # Load source and target fragments
        source_obj = load_fragment(source)
        target_obj = load_fragment(target)

        # Apply the transformations
        apply_transformation(source_obj, transformation)
        apply_transformation(target_obj, transformation)

        # Add them to the list of fragments
        loaded_fragments.extend([source_obj, target_obj])

    # Merge all fragments into one object
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()  # Merge selected objects

    # Optional: Clean up (e.g., remove duplicates, recalculate normals)
    # Switch to Edit Mode (important for background mode)
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.mode_set(mode='EDIT')

    # Remove doubles (merge vertices that are too close)
    bpy.ops.mesh.remove_doubles()

    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Optional: Smooth shading for a nicer look
    bpy.ops.object.shade_smooth()

    # Export the merged object to a file
    bpy.ops.export_mesh.ply(filepath=OUTPUT_PATH)

    print(f"Reconstruction complete. Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
