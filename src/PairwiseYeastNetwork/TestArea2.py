import torch
import torch.nn as nn
import torch.nn.functional as F

import os

# outputs = torch.tensor([[-10.0,7.0,-9.0]],dtype=torch.float32)

# targets = torch.tensor([[0.0,0.0,1.0]],dtype=torch.float32)

# outputs = torch.tensor([[5.0,-1.0,4.0],[-10.0,7.0,-9.0]],dtype=torch.float32)

# targets = torch.tensor([[1.0,0.0,1.0],[0.0,0.0,1.0]],dtype=torch.float32)

# bce = nn.BCEWithLogitsLoss(reduction='none')

# pos = targets == 1
# neg = targets == 0

# print(outputs.size(dim=0))

# pos_scores = [outputs[i][targets[i] == 1] for i in range(outputs.size(dim=0))]
# neg_scores = [outputs[i][targets[i] == 0] for i in range(outputs.size(dim=0))]



# zlpr = [torch.log(1 + torch.sum(torch.exp(-pos_scores[i]))) + torch.log(1 + torch.sum(torch.exp(neg_scores[i]))) for i in range(outputs.size(dim=0))]
# print(1 + torch.sum(torch.exp(-pos_scores)))
# print(1 + torch.sum(torch.exp(neg_scores)))

# print(zlpr)
# print(torch.sum(zlpr))

# print(torch.mean(bce(outputs,targets)))

print(os.path.dirname(__file__))

