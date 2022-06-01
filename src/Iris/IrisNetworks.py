import torch
import torch.nn as nn
import torch.nn.functional as F

#Perceptron with no hidden layers
class IrisNet4x3(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = '4 x 3'
        self.l1 = nn.Linear(4,3)

    def forward(self,x):
        x = self.l1(x)
        return x

class IrisNet4x2x3(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = '4 x 2 x 3'
        self.l1 = nn.Linear(4,2)
        self.l2 = nn.Linear(2,3)

    def forward(self,x):
        x = F.relu(self.l1(x))
        x = self.l2(x)
        return x

class IrisNet4x3x3x3(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = '4 x 3 x 3 x 3'
        self.l1 = nn.Linear(4,3)
        self.l2 = nn.Linear(3,3)
        self.l3 = nn.Linear(3,3)

    def forward(self,x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = self.l3(x)
        return x