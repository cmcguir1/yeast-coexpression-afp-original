import numpy as np
from tempfile import mkdtemp
import os.path as path
import torch
import torch.nn.functional as nn

bce_reduce = torch.nn.BCEWithLogitsLoss(reduction='none')
bce = torch.nn.BCEWithLogitsLoss(reduction='mean')
features = torch.tensor([[1000,1000,20],[100,200,20]])
labels = torch.tensor([[1,0,1],[1,0,0]])
loss_reduce = bce_reduce(features.float(),labels.float())
loss = bce(features.float(),labels.float())
for row in torch.transpose(loss_reduce,0,1):
    print(torch.mean(row).item())




