import open3d as o3d
from pathlib import Path
import numpy as np

def visualize_fragments(folder, voxel_size=0.5):
    folder = Path(folder)
    meshes = []
    cols = 4
    grid_spacing = 250

    ply_files = sorted(folder.glob("*.ply"))
    print(f"Loading {len(ply_files)} aligned pieces...")

    for idx, ply_path in enumerate(ply_files):
        mesh = o3d.io.read_triangle_mesh(str(ply_path))
        if mesh.is_empty():
            continue

        mesh.compute_vertex_normals()

        # Apply mild downsampling (optional)
        if voxel_size > 0:
            mesh = mesh.simplify_vertex_clustering(
                voxel_size=voxel_size,
                contraction=o3d.geometry.SimplificationContraction.Average
            )

        # Place in grid
        row, col = divmod(idx, cols)
        mesh.translate((col * grid_spacing, -row * grid_spacing, 0))

        # Add bounding box for better visualization
        bbox = mesh.get_axis_aligned_bounding_box()
        bbox.color = (1, 0, 0)
        meshes.append(mesh)
        meshes.append(bbox)

    print("Launching viewer...")
    o3d.visualization.draw_geometries(meshes)

if __name__ == "__main__":
    visualize_fragments("/home/kira/Desktop/healing_stones/aligned", voxel_size=1.0)
