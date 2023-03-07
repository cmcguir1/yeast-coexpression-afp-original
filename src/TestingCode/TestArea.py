from __future__ import generator_stop
import sys
import pandas as pd
import torch


sys.path.insert(0,'./obopy')
from Leaf import getLeaves

def key(leaf):
    return len(leaf[1])

leaves = getLeaves(10)
leafTable = []
for leaf in leaves:
    leafTable.append([leaf[0],key(leaf)])

sortedLeaves = sorted(leafTable,key=lambda x: x[1])
for leaf in sortedLeaves:
    print(f'{leaf[0]}: {leaf[1]}')

