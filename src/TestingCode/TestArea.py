from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

outputs = torch.ones(size=(1,10))
labels = torch.zeros(size=(1,10))
labels[0,0] = 1.0
labels[0,2] = 1.0
#weights = torch.ones(size=(10,))
weights = torch.tensor([10,1,1,1,1,1,1,1,1,1])

loss = nn.CrossEntropyLoss()
weightedLoss = nn.CrossEntropyLoss(weight=weights)


print(f'Loss: {loss(outputs,labels)}')
print(f'Weighted Loss: {weightedLoss(outputs,labels)}')