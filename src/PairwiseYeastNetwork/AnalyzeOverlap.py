from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np

sys.path.insert(0,'./obopy')
from Leaf import getLeaves

leaves = getLeaves(10)
leafDict = {}
for leaf in leaves:
    leafDict[leaf[0]] = leaf[1]

termArray = pd.read_csv('./src/PairwiseYeastNetwork/TermNameDict.csv').to_numpy()
termDict = {}
for term in termArray:
    termDict[term[0]] = term[1]

GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
GOTermDict = {term[0]: int(term[1]) for term in GoTerms}
GOTermIndexDict = {int(term[1]): term[0] for term in GoTerms}

overLap = pd.read_csv('./Yeast Resources/OverlapResults/Overlap.csv').to_numpy()


num = int(input('How many terms would you like to display: '))
response = input('Term to search: ')
print(f'\nTerms with highest overalp with {response} ({termDict[response]})\n')
while response != 'q':
    if response in GOTermDict:
        termIndex = GOTermDict[response]
        indices = np.argsort(overLap[termIndex])
        for i in range(0,num+1):
            # print(GOTermIndexDict[indices[i]])
            # print(GOTermDict[termIndexDict[indices[i]]])
            # print(overLap[termIndex,indices[i]])
            print(f'{i+1}.\tTerm: {GOTermIndexDict[indices[i]]} ({termDict[GOTermIndexDict[indices[i]]]})')
            print(f'\tp-value: {overLap[termIndex,indices[i]]}')
            print(f'\tOverlapping Genes: {len(leafDict[GOTermIndexDict[indices[i]]] & leafDict[response])} / {len(leafDict[GOTermIndexDict[indices[i]]])}\n')
    else:
        print('Invalid term')
    response = input('Term to search: ')

