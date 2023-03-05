from __future__ import generator_stop
import sys
import pandas as pd
import torch


loss = torch.nn.CrossEntropyLoss()
features = torch.tensor([[0.9,0.5,0.1,0.5,0.2]],dtype=float)
# features = torch.tensor([[20,1000,0,1000,0]],dtype=float)
labels = torch.tensor([[0,1,0,1,0]],dtype=float)
print(loss(features,labels).item())
