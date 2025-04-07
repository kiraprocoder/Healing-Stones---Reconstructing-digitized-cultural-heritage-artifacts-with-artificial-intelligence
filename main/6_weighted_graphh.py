import open3d as o3d
import numpy as np
from pathlib import Path
import itertools
from tqdm import tqdm

# ---------- Parameters ----------
VOXEL_SIZE = 2.0  # downsample for FPFH
RANSAC_DISTANCE = 5.0  # threshold for RANSAC match

# ---------- Feature Extraction ----------
def preprocess_fragment(pcd, voxel_size):
    pcd_down = pcd.voxel_down_sample(voxel_size)
    pcd_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 2, max_nn=30))
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=voxel_size * 5, max_nn=100)
    )
    return pcd_down, fpfh

# ---------- Pairwise Matching ----------
def compute_match_score(source_down, target_down, source_fpfh, target_fpfh):
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down,
        source_fpfh, target_fpfh,
        mutual_filter=True,
        max_correspondence_distance=RANSAC_DISTANCE,
        estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        ransac_n=4,
        checkers=[
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(RANSAC_DISTANCE)
        ],
        criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(40000, 500)
    )
    return result.fitness  # Higher = better match

# ---------- Build Graph ----------
def build_matching_graph(ply_folder):
    ply_files = sorted(Path(ply_folder).glob("*.ply"))
    fragments = {}
    descriptors = {}

    print("Preprocessing fragments for feature extraction...")
    for ply in tqdm(ply_files):
        pcd = o3d.io.read_point_cloud(str(ply))
        down, fpfh = preprocess_fragment(pcd, VOXEL_SIZE)
        fragments[ply.stem] = down
        descriptors[ply.stem] = fpfh

    graph = []
    print("Computing pairwise match scores...")
    for (a_name, b_name) in tqdm(itertools.combinations(fragments.keys(), 2)):
        a_down = fragments[a_name]
        b_down = fragments[b_name]
        a_fpfh = descriptors[a_name]
        b_fpfh = descriptors[b_name]

        score = compute_match_score(a_down, b_down, a_fpfh, b_fpfh)
        graph.append((a_name, b_name, score))

    return graph

if __name__ == "__main__":
    ply_folder = "/home/kira/Desktop/healing_stones/aligned"
    graph = build_matching_graph(ply_folder)

    # Save graph to disk
    import json
    with open("match_graph.json", "w") as f:
        json.dump(graph, f, indent=2)

    print("Graph constructed with", len(graph), "edges.")
