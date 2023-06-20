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


interactions = pd.read_csv('./BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.222.tab.txt',sep='\t').to_numpy()
# print(len([0 for row in interactions ]))
map = {}
for system in set(interactions[:,6]):
    map[system] = 0

for row in interactions:
    map[row[6]] += 1

for system, num in map.items():
    print(f'{system}: {num}')