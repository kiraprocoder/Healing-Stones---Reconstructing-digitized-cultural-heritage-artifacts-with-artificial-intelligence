import numpy as np
import open3d as o3d
import os
from pathlib import Path

def analyze_ply_file(file_path):
    """Analyze a PLY file and return key metrics"""
    mesh = o3d.io.read_triangle_mesh(file_path)
    
    if mesh.is_empty():
        print(f"Warning: {file_path} is empty or unreadable.")
        return None, None

    num_vertices = len(mesh.vertices)
    num_triangles = len(mesh.triangles)
    
    # Bounding box dimensions
    bbox = mesh.get_axis_aligned_bounding_box()
    dimensions = bbox.get_max_bound() - bbox.get_min_bound()
    
    # Center of mass (approximate)
    center = np.mean(np.asarray(mesh.vertices), axis=0)
    
    # Compute normals and surface area
    mesh.compute_vertex_normals()
    area = mesh.get_surface_area()
    
    # Compute average normal, handling zero division
    avg_normal = np.mean(np.asarray(mesh.vertex_normals), axis=0)
    norm_value = np.linalg.norm(avg_normal)
    avg_normal = avg_normal / norm_value if norm_value != 0 else np.array([0, 0, 0])
    
    return {
        "filename": os.path.basename(file_path),
        "vertices": num_vertices,
        "triangles": num_triangles,
        "dimensions": dimensions,
        "center": center,
        "surface_area": area,
        "avg_normal": avg_normal
    }, mesh

def analyze_folder(folder_path):
    """Analyze all PLY files in a folder (case-insensitive)"""
    folder = Path(folder_path)
    ply_files = [f for f in folder.iterdir() if f.suffix.lower() == ".ply"]
    results = []

    for file_path in ply_files:
        print(f"Analyzing {file_path.name}...")
        result, _ = analyze_ply_file(str(file_path))
        if result:
            results.append(result)
    
    return results

if __name__ == "__main__":
    folder_path = "/home/kira/Desktop/healing_stones/mats/3D"
    results = analyze_folder(folder_path)
    
    for res in results:
        print(res)
