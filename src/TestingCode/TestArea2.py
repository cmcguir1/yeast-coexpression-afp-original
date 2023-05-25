from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import time
import os

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

leaves = getLeaves(10,bioProc=True,dataset='original')
allGenes = getGenes('GO:0008150',dataset='original')

names = pd.read_csv('./src\PairwiseYeastNetwork/TermNameDict.csv').to_numpy()
namesDict = {name[0]: name[1] for name in names}

pairs = []
for i in range(len(allGenes)):
    for j in range(i+1,len(allGenes)):
        pairs.append([allGenes[i],allGenes[j]])

multiCoAnnos = 0
mca_list = []
coAnnos = 0
for pair in pairs:
    annos = 0
    coAnnosList = []
    for leaf in leaves:
        if pair[0] in leaf[1] and pair[1] in leaf[1]:
            annos += 1
            coAnnosList.append(namesDict[leaf[0]])
    if annos != 0:
        coAnnos += 1
    if annos > 1:
        multiCoAnnos += 1
        mca_list.append(coAnnosList)

finalList = []
_ = [finalList.append(item) for item in mca_list if not (item in finalList)]

print(f'Total Pairs: {len(pairs)}')
print(f'Pairs Co-annotated to any GO Term: {coAnnos}')
print(f'Percentage of Co-annotations: {(coAnnos/len(pairs))*100}%')
print(f'Pairs Co-annotated to multiple GO Terms: {multiCoAnnos}')
print(f'Percentage of multiple Co-annotations {(multiCoAnnos/len(pairs))*100}%')
pd.DataFrame(finalList).to_csv('./CoAnnos.csv',index=False)


