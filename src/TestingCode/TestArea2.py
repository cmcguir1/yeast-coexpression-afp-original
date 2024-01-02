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

leaves = getLeaves(10,dataset='original',exclude=['GO:0002181','GO:0022857','GO:0032543'])
genes = set()
for leaf in leaves:
    if leaf[0] == 'GO:0007005':
        print(f'Mito: {len(leaf[1])}')
    genes = genes.union(leaf[1])

print(len(leaves))
print(len(genes))


# genes_2009 = getGenes('GO:0007005',dataset='2007')
# genes_modern = getGenes('GO:0007005',dataset='modern')
# print(f'2007: {len(genes_2007)}')

# print(f'2023: {len(genes_modern)}')

# genes_2007 = getGenes('GO:0000001',dataset='2007')
# genes_2009 = getGenes('GO:0000001',dataset='2009')
# genes_modern = getGenes('GO:0000001',dataset='modern')
# print(f'2007: {len(genes_2007)}')
# print(f'2009: {len(genes_2009)}')
# print(f'2023: {len(genes_modern)}')


