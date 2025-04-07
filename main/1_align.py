import numpy as np
import open3d as o3d
from pathlib import Path


def get_rotation_matrix(normal_vector):
    """Compute rotation matrix to align normal vector to the Z-axis."""
    normal_vector = normal_vector / np.linalg.norm(normal_vector)  # Normalize

    theta_x = np.arcsin(normal_vector[1] / np.linalg.norm([normal_vector[1], normal_vector[2]]))
    theta_y = np.arcsin(normal_vector[0] / np.linalg.norm([normal_vector[0], normal_vector[2]]))
    
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(theta_x), -np.sin(theta_x)],
        [0, np.sin(theta_x), np.cos(theta_x)]
    ])
    
    Ry = np.array([
        [np.cos(theta_y), 0, np.sin(theta_y)],
        [0, 1, 0],
        [-np.sin(theta_y), 0, np.cos(theta_y)]
    ])
    
    return np.dot(Ry, Rx)


def align_mesh(file_path, output_path):
    """Aligns the mesh based on its dominant normal direction."""
    print(f"\nProcessing: {file_path}")  

    # Load mesh
    mesh = o3d.io.read_triangle_mesh(file_path)
    if mesh.is_empty():
        print(f"Skipping {file_path}: Invalid or empty mesh.")
        return
    
    # Convert mesh to point cloud for plane segmentation
    pcd = mesh.sample_points_uniformly(number_of_points=100000)
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamKNN(knn=30))

    # Segment largest plane
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.2, ransac_n=5, num_iterations=1000)
    
    if len(inliers) == 0:
        print(f"Skipping {file_path}: No significant plane detected.")
        return

    normal_vector = np.array(plane_model[:3])  # Extract normal from plane equation
    print(f"Aligning {file_path} | Normal Vector: {normal_vector}")

    # Compute rotation
    R = get_rotation_matrix(normal_vector)
    mesh.rotate(R, center=(0, 0, 0))
    
    # Save aligned mesh
    o3d.io.write_triangle_mesh(output_path, mesh)
    print(f"Aligned mesh saved to {output_path}")


def process_folder(input_folder, output_folder):
    """Processes all PLY files in a given folder."""
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\nProcessing folder: {input_folder}")
    files = list(input_path.glob("*.ply")) + list(input_path.glob("*.PLY"))
    
    if not files:
        print("No PLY files found in the directory.")
        return

    for ply_file in files:
        output_file = output_path / f"{ply_file.stem}_aligned.ply"
        align_mesh(str(ply_file), str(output_file))


if __name__ == "__main__":
    input_folder = "/home/kira/Desktop/healing_stones/mats/3D"
    output_folder = "/home/kira/Desktop/healing_stones/aligned"
    process_folder(input_folder, output_folder)