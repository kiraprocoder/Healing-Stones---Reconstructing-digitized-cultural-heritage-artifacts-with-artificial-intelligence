import torch
import json
import itertools
from model import FragmentMatcher
import torch.nn as nn

# Load descriptors
with open("fragment_descriptors.json", "r") as f:
    descriptors = json.load(f)

# Prepare device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
model = FragmentMatcher().to(device)
model.load_state_dict(torch.load("trained_fragment_matcher.pth", map_location=device))
model.eval()

# Pairwise match prediction
matches = []
fragment_ids = list(descriptors.keys())

for frag_a, frag_b in itertools.combinations(fragment_ids, 2):
    desc_a = torch.tensor(descriptors[frag_a]).float().unsqueeze(0).to(device)
    desc_b = torch.tensor(descriptors[frag_b]).float().unsqueeze(0).to(device)

    with torch.no_grad():
        score = model(desc_a, desc_b).item()

    matches.append({
        "fragment_A": frag_a,
        "fragment_B": frag_b,
        "score": score
    })

# Sort by score descending
matches.sort(key=lambda x: x["score"], reverse=True)

# Save matches
with open("predicted_matches.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"Saved {len(matches)} predicted matches to predicted_matches.json")
