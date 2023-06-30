import torch
import numpy as np
from FocalLoss import FocalLoss
from CustomCrossEntropyLoss import CustomCrossEntropyLoss
import torch.nn.functional as F
import pandas as pd
import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

labels = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]])
randomized = np.random.permutation(labels)
print(f'Labels:\n{labels}')
print(f'Randomized:\n{randomized}')

# interactionsList = pd.read_csv('./GeneticInteractions_Original.csv').to_numpy().flatten()
# print(interactionsList)
# interactions = pd.read_csv('../BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.222.tab.txt',sep='\t').to_numpy()
# # interactions = pd.read_csv('./InteractionData.txt',sep='\t').to_numpy()

# # print(len([0 for row in interactions ]))
# map = {}
# for system in set(interactions[:,6]):
#     map[system] = 0

# for row in interactions:
#     map[row[6]] += 1

# for system, num in map.items():
#     if num >= 5000:
#         print(f'{system}: {num}')