import torch
from model import FragmentMatcher
from data_loader import get_dataloader
import torch.nn as nn

def evaluate(model_path="trained_fragment_matcher.pth"):
    json_path = "match_graph.json"
    descriptor_path = "fragment_descriptors.json"
    dataloader = get_dataloader(json_path, descriptor_path)

    model = FragmentMatcher()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    criterion = nn.MSELoss()
    total_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for source, target, label in dataloader:
            output = model(source, target).squeeze()
            label = label.squeeze()

            loss = criterion(output, label)
            total_loss += loss.item()

            predicted = (output >= 0.5).float()
            correct += (predicted == label).sum().item()
            total += label.numel()

    print(f"Evaluation Loss: {total_loss:.4f}")
    print(f"Accuracy: {(correct / total) * 100:.2f}%")

if __name__ == "__main__":
    evaluate()
