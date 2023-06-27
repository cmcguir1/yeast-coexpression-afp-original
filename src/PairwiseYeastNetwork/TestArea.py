import torch
import numpy as np
from FocalLoss import FocalLoss
from CustomCrossEntropyLoss import CustomCrossEntropyLoss
import torch.nn.functional as F
import pandas as pd
import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

# redo = np.memmap()
l = torch.nn.LogSoftmax(dim=1)
nll = torch.nn.NLLLoss()

targets = torch.tensor([[1,0,0]],dtype=torch.float)
output = torch.tensor([[20,10,2]],dtype=torch.float)
print(f'Cross Entropy: {F.cross_entropy(output,targets)}')
print(f'Custom Cross Entropy: {nll(l(output),targets)}')

# interactions = pd.read_csv('./BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.222.tab.txt',sep='\t').to_numpy()
# # print(len([0 for row in interactions ]))
# map = {}
# for system in set(interactions[:,6]):
#     map[system] = 0

# for row in interactions:
#     map[row[6]] += 1

# for system, num in map.items():
#     print(f'{system}: {num}')