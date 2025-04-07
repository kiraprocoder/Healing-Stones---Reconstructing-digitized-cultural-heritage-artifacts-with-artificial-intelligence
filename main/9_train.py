import torch
import torch.nn as nn
import torch.optim as optim
from model import FragmentMatcher
from data_loader import get_dataloader

def train():
    graph_path = "match_graph.json"
    descriptor_path = "fragment_descriptors.json"

    dataloader = get_dataloader(graph_path, descriptor_path)
    print(f"Loaded dataloader with {len(dataloader.dataset)} samples")

    model = FragmentMatcher()
    criterion = nn.MSELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    model.train()
    for epoch in range(136):
        total_loss = 0
        for source_feat, target_feat, label in dataloader:
            pred = model(source_feat, target_feat)
            label = label.view(-1) 
            loss = criterion(pred, label)


            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1} | Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), "trained_fragment_matcher.pth")
    print("Model saved as trained_fragment_matcher.pth")

if __name__ == "__main__":
    train()
