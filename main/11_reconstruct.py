import open3d as o3d
import json
import os
import numpy as np

FRAGMENT_FOLDER = "/home/kira/Desktop/healing_stones/aligned"
MATCHES_PATH = "aligned_matches.json"

def load_fragments(folder):
    fragments = {}
    for file in os.listdir(folder):
        if file.endswith(".ply"):
            name = os.path.splitext(file)[0]
            path = os.path.join(folder, file)
            pcd = o3d.io.read_point_cloud(path)
            pcd.estimate_normals()
            fragments[name] = pcd
    return fragments

def main():
    with open(MATCHES_PATH, "r") as f:
        matches = json.load(f)

    fragments = load_fragments(FRAGMENT_FOLDER)

    # Create a transformed point cloud list
    combined = o3d.geometry.PointCloud()
    placed = set()

    for match in matches:
        source_id = match["fragment_A"]
        target_id = match["fragment_B"]
        transformation = np.array(match["transformation"])

        source = fragments[source_id]
        target = fragments[target_id]

        if target_id not in placed:
            fragments[target_id] = target
            placed.add(target_id)
            combined += target

        # Transform and add source
        transformed_source = source.transform(transformation)
        fragments[source_id] = transformed_source
        combined += transformed_source
        placed.add(source_id)

    print(f"Visualizing {len(placed)} aligned fragments...")
    o3d.visualization.draw_geometries([combined])

if __name__ == "__main__":
    main()
