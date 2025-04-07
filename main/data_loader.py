import json
import torch
from torch.utils.data import Dataset, DataLoader

class MatchGraphDataset(Dataset):
    def __init__(self, graph_path, descriptor_path):
        with open(graph_path, 'r') as f:
            self.edges = json.load(f)
        with open(descriptor_path, 'r') as f:
            self.descriptors = json.load(f)

    def __len__(self):
        return len(self.edges)

    def __getitem__(self, idx):
        source_name, target_name, label = self.edges[idx]

        source_feat = torch.tensor(self.descriptors[source_name], dtype=torch.float32)
        target_feat = torch.tensor(self.descriptors[target_name], dtype=torch.float32)
        label = torch.tensor([label], dtype=torch.float32)

        return source_feat, target_feat, label

def get_dataloader(graph_path, descriptor_path, batch_size=8):
    dataset = MatchGraphDataset(graph_path, descriptor_path)
    return DataLoader(dataset, batch_size=batch_size, shuffle=True)
