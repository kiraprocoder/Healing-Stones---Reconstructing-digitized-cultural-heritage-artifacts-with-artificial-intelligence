import open3d as o3d
import numpy as np
from pathlib import Path

def load_downsampled_meshes(folder, voxel_size=1.0):
    path = Path(folder)
    ply_files = list(path.glob("*.ply"))
    meshes = []
    for file in ply_files:
        mesh = o3d.io.read_triangle_mesh(str(file))
        if not mesh.is_empty():
            mesh = mesh.simplify_vertex_clustering(
                voxel_size=voxel_size,
                contraction=o3d.geometry.SimplificationContraction.Average
            )
            mesh.remove_unreferenced_vertices()
            mesh.compute_vertex_normals()
            meshes.append((mesh, file.name))
        else:
            print(f"Skipping empty mesh: {file.name}")
    return meshes


def arrange_in_grid(meshes, spacing=100):
    num = len(meshes)
    cols = int(np.ceil(np.sqrt(num)))
    rows = int(np.ceil(num / cols))

    arranged = []
    for i, (mesh, _) in enumerate(meshes):
        row, col = divmod(i, cols)
        bbox = mesh.get_axis_aligned_bounding_box()
        size = bbox.get_extent()

        tx = col * (spacing + size[0])
        ty = row * (spacing + size[1])
        translated = mesh.translate((tx, ty, 0), relative=False)
        arranged.append(translated)
    
    return arranged


if __name__ == "__main__":
    folder = "/home/kira/Desktop/healing_stones/aligned"
    print("Loading aligned fragments ")
    meshes = load_downsampled_meshes(folder, voxel_size=2.0)

    if not meshes:
        print("No meshes found.")
        exit()

    print("Arranging...")
    grid = arrange_in_grid(meshes)
    
    print("Visualizing...")
    o3d.visualization.draw_geometries(grid)
