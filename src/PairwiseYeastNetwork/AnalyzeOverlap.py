from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import math

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

def analyzeOverlap():
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

def rankSimilarity():
    absList = []
    disList = []
    sigList = []
    for term, index in GOTermDict.items():
        discreteTotal = 0
        absoluteTotal = 0
        sigTotal = 0
        for i in range(len(overLap)):
            if i != index:
                absoluteTotal += overLap[index,i]
                sigTotal += (1/(1+np.exp(-overLap[index,i])))
                if overLap[index,i] <= .01:
                    discreteTotal += 1
    
        absList.append([term,absoluteTotal])
        disList.append([term,discreteTotal])
        sigList.append([term,sigTotal])
    sortedAbs = sorted(absList,key=lambda item: item[1])
    sortedDis = sorted(disList,key=lambda item: item[1],reverse=True)
    sortedSig = sorted(sigList,key=lambda item: item[1])
    
    print('Absolute Sums:')
    for i, row in enumerate(sortedAbs):
        print(f'\t{i}. {row[0]} {row[1]} ({termDict[row[0]]})')

    print('Sigmoidal Sums:')
    for i, row in enumerate(sortedSig):
        print(f'\t{i}. {row[0]} {row[1]} ({termDict[row[0]]})')

    print('Discrete Cutoff:')
    for i, row in enumerate(sortedDis):
        print(f'\t{i}. {row[0]} {row[1]} ({termDict[row[0]]})')
    

rankSimilarity()







