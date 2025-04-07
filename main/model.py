import torch.nn as nn
import torch
import torch.nn.functional as F

class FragmentMatcher(nn.Module):
    def __init__(self, input_dim=33, hidden_dim=128):
        super(FragmentMatcher, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2)
        )
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

    def forward(self, x1, x2):
        embed1 = self.encoder(x1)
        embed2 = self.encoder(x2)
        combined = torch.cat([embed1, embed2], dim=1)
        out = self.classifier(combined)
        return out.squeeze()

