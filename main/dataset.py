import json
import torch
from torch.utils.data import Dataset

class MatchGraphDataset(Dataset):
    def __init__(self, json_path):
        with open(json_path, "r") as f:
            self.edges = json.load(f)

    def __len__(self):
        return len(self.edges)

    def __getitem__(self, idx):
        source, target, score = self.edges[idx]
        
        # Dummy label as tensor
        label = torch.tensor([score], dtype=torch.float32)

        return source, target, label
