from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import torch


sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes



leaves = getLeaves(10)
alpha = []
for leaf in leaves:
    num = len(leaf[1]) * len(leaf[1]) - len(leaf[1])
    alpha.append([leaf[0],33681465/num])
print(alpha)



# scores = np.memmap('D:/AllScoreMemMap.dat',dtype='float32',shape=(27830900+5850565,92),mode='r+')
# pairs = np.memmap('D:/AllPairs.dat',shape=(27830900+5850565,2),dtype='U10',mode='r+')

# print(scores)
# print(pairs)
# print(scores)
# offset = 27830900
# for i in range(4):
#     print(f"Started Loading fold {i}")
#     data = pd.read_csv(f'./agnScores_fold{i}.csv').to_numpy()
#     print(f"Loaded fold {i}")
#     scores[offset:offset+len(data),:] += (data[:,2:] / 4.0).astype('float32')
#     if(i == 0):
#         pairs[offset:offset+len(data),:] = data[:,:2]
#     del data



