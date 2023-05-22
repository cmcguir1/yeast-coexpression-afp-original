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

leaves = getLeaves(10,bioProc=False,molFunc=True,cellComp=False)
names = pd.read_csv('./src/PairwiseYeastNetwork/TermNameDict.csv').to_numpy()
namesDict = {}
for row in names:
    namesDict[row[0]] = row[1]

for leaf in leaves:
    print(f'{leaf[0]}: {namesDict[leaf[0]]}')