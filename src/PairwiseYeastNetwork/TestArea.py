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

arr1 = np.array([0.1,0.2,0.3],dtype=np.float32)
arr2 = np.array([0.1,0.2,0.3],dtype=np.float32)
print(arr1 == arr2)
print(arr1)
print(arr2)

# interactions = pd.read_csv('./BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.222.tab.txt',sep="\t").to_numpy()
# systems = set()
# total = 0
# for row in interactions:
#     if (row[6] == 'Negative Genetic' or row[6] == 'Positive Genetic') and row[7] == 'Costanzo M (2016)':
#         total += 1
#     systems.add(row[6])
# print(systems)
# print(len(interactions))
# print(total)

# mat = pd.read_csv('./SGA_ExE_clustered.cdt',sep='\t').to_numpy()
# print(mat)
