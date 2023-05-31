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

leaves = getLeaves(10,bioProc=True,dataset='modern')

termArray = pd.read_csv('./src/PairwiseYeastNetwork/TermNameDict.csv').to_numpy()
termDict = {}
for term in termArray:
    termDict[term[0]] = term[1]
allGenes = getGenes('GO:0008150',dataset='original')

allGenesMap = {}
for gene in allGenes:
    annos = set()
    for leaf in leaves:
        if gene in leaf[1]:
            annos.add(leaf[0] + ": " + termDict[leaf[0]])
    allGenesMap[gene] = annos


again = True
while again:
    userGene = input("Gene: ")
    if userGene == 'q':
        again = False
    else:
        if len(allGenesMap[userGene]) == 0:
            print("This gene does not have any annotations in the GO Slim")
        else:
            print("")
            for term in allGenesMap[userGene]:
                print(f'\t{term}')
            print("")


