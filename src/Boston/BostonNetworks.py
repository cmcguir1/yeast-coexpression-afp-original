import torch.nn as nn
import torch.nn.functional as F

#13 x 3 x 1 Network
class BostonNet1(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = '13 x 3 x 1'
        self.h1 = nn.Linear(13,3)
        self.h2 = nn.Linear(3,1)
    
    def forward(self,x):
        x = F.relu(self.h1(x))
        x = self.h2(x)
        return x

#13 x 5 x 1 Network
class BostonNet2(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = '13 x 5 x 1'
        self.h1 = nn.Linear(13,5)
        self.h2 = nn.Linear(5,1)

    def forward(self,x):
        x = F.relu(self.h1(x))
        x = self.h2(x)
        return x

#13 x 5 x 5 x 1 Netowrk
class BostonNet3(nn.Module):
    def __init__(self):
        super().__init__()
        self.structure = '13 x 5 x 5 x 1'
        self.h1 = nn.Linear(13,5)
        self.h2 = nn.Linear(5,5)
        self.h3 = nn.Linear(5,1)

    def forward(self,x):
        x = F.relu(self.h1(x))
        x = F.relu(self.h2(x))
        x = self.h3(x)
        return x

