from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import time
import os

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes, printName

bioProc = getLeaves(10,dataset='modern',exclude=['GO:0002181','GO:0022857','GO:0032543'])
# cellComp = getLeaves(10,dataset='modern',exclude=['GO:0002181','GO:0022857','GO:0032543'],cellComp=True,bioProc=False)
# molFunc = getLeaves(10,dataset='modern',exclude=['GO:0002181','GO:0022857','GO:0032543'],molFunc=True,bioProc=False)

# all = getLeaves(10,dataset='modern',exclude=['GO:0002181','GO:0022857','GO:0032543'],cellComp=True,molFunc=True)

def info(leaves):
    print(f'Number of terms: {len(leaves)}')
    genes = set()
    for leaf in leaves:
        genes = genes.union(leaf[1])
    print(f'Genes: {len(genes)}')

# print('Bio Proc')
# info(bioProc)
# print('\nCell Comp')
# info(cellComp)
# print('\nMol Func')
# info(molFunc)
# print('\nAll Branches')
# info(all)



# data = pd.read_csv('src\PairwiseYeastNetwork\AllGOGeneFold_Original_bce_1.csv').to_numpy()
# data = pd.read_csv('src\PairwiseYeastNetwork\AllGOGeneFold_Modern_bce_1.csv').to_numpy()


# folds = [set(),set(),set(),set()]
# for row in data:
#     folds[row[1]].add(row[0])

# for fold in folds:
#     print(len(fold & genes))
# name = {row[0]:row[1] for row in pd.read_csv('src\PairwiseYeastNetwork\TermNameDict.csv').to_numpy()}

# leaves = getLeaves(10,dataset='2007',exclude=['GO:0002181','GO:0022857','GO:0032543'],molFunc=True,cellComp=True,bioProc=True)
# # leaves = getLeaves(10,dataset='modern',molFunc=True,cellComp=True)
# genes = set()
# for leaf in leaves:
    
#     genes = genes.union(leaf[1])

# print(f'Terms: {len(leaves)}')
# print(f'Genes: {len(genes)}')

# folds = pd.read_csv('./src/PairwiseYeastNetwork/AllGOGeneFold_Original_1.csv').to_numpy()



# lst = [0,0,0,0]
# for gene in folds:
#     if gene[0] in genes:
#         lst[gene[1]] += 1

# print(lst)
# genes_modern = getGenes('GO:0007005',dataset='modern')
# print(f'2007: {len(genes_2007)}')

# print(f'2023: {len(genes_modern)}')

# genes_2007 = getGenes('GO:0000001',dataset='2007')
# genes_2009 = getGenes('GO:0000001',dataset='2009')
# genes_modern = getGenes('GO:0000001',dataset='modern')
# print(f'2007: {len(genes_2007)}')
# print(f'2009: {len(genes_2009)}')
# print(f'2023: {len(genes_modern)}')


