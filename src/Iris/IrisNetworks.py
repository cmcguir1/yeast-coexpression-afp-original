import torch
import torch.nn as nn

class IrisNet4x3(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = '4 x 3'
        self.h1 = nn.Linear(4,3)

    def forward(self,x):
        x = self.h1(x)
        return x
