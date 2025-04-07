import open3d as o3d
import json
import os

FRAGMENT_FOLDER = "/home/kira/Desktop/healing_stones/aligned"  # Adjust this if needed
MATCHES_PATH = "top_matches.json"
OUTPUT_PATH = "aligned_matches.json"

def load_point_cloud(name):
    path = os.path.join(FRAGMENT_FOLDER, f"{name}.ply")
    pcd = o3d.io.read_point_cloud(path)
    pcd.estimate_normals()
    return pcd

def align_fragments(source, target):
    threshold = 0.02  # Adjust this based on scale
    reg = o3d.pipelines.registration.registration_icp(
        source, target, threshold,
        np.eye(4),
        o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )
    return reg.transformation

def main():
    with open(MATCHES_PATH, "r") as f:
        matches = json.load(f)

    aligned_matches = []

    for match in matches:
        source_id = match["source"]
        target_id = match["target"]

        source_pcd = load_point_cloud(source_id)
        target_pcd = load_point_cloud(target_id)

        transformation = align_fragments(source_pcd, target_pcd)

        aligned_matches.append({
            "fragment_A": source_id,
            "fragment_B": target_id,
            "score": match["score"],
            "transformation": transformation.tolist()
        })

    with open(OUTPUT_PATH, "w") as f:
        json.dump(aligned_matches, f, indent=2)

    print(f"Saved aligned matches to {OUTPUT_PATH}")

if __name__ == "__main__":
    import numpy as np
    main()
