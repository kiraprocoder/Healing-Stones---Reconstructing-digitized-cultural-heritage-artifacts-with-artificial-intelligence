import open3d as o3d
import numpy as np
import os
import json
from pathlib import Path

def extract_fpfh(pcd):
    radius_normal = 0.05
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    
    radius_feature = 0.1
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100)
    )
    return fpfh.data.mean(axis=1)  # Use mean feature vector as descriptor

def process_folder(folder_path, save_path):
    descriptors = {}
    for file in Path(folder_path).glob("*.ply"):
        mesh = o3d.io.read_triangle_mesh(str(file))
        if mesh.is_empty():
            continue
        pcd = mesh.sample_points_uniformly(number_of_points=5000)
        descriptor = extract_fpfh(pcd)
        descriptors[file.stem] = descriptor.tolist()
    
    with open(save_path, 'w') as f:
        json.dump(descriptors, f, indent=4)
    print(f"Saved descriptors to {save_path}")

if __name__ == "__main__":
    input_dir = "/home/kira/Desktop/healing_stones/aligned"
    output_file = "fragment_descriptors.json"
    process_folder(input_dir, output_file)
