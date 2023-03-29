from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import torch


sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

# def key(leaf):
#     return len(leaf[1])

# termArray = pd.read_csv('./src/PairwiseYeastNetwork/TermNameDict.csv').to_numpy()
# termDict = {}
# for term in termArray:
#     termDict[term[0]] = term[1]

# 
# for i,leaf in enumerate(leaves):
#     print(f'{i}: {leaf[0]}')

folds = [pd.read_csv(f'./Yeast Resources/GraphResults/NewRank/posScores_fold{i}.csv').to_numpy(dtype=object) for i in range(4)]
genePairs = np.concatenate(folds,axis=0)

leaves = getLeaves(10)
pos = getGenes('GO:0007005',dataset='original')
neg = set()
for leaf in leaves:
    if leaf[0] != 'GO:00070005':
        neg = neg | leaf[1]

lst = []
for pair in genePairs:
    if pair[0] in pos and pair[1] in pos:
        lst.append([pair[0],pair[1],1,pair[2]])
    elif (pair[0] in pos and pair[1] in neg) or (pair[0] in neg and pair[1] in pos):
        lst.append([pair[0],pair[1],-1,pair[2]])
    elif pair[0] in neg and pair[1] in neg:
        lst.append([pair[0],pair[1],-1,pair[2]])
print('Began Sorting')
sorted(lst,key=lambda row: row[3],reverse=True)
pd.DataFrame(lst,columns=['Gene 1','Gene2','Label','Score']).to_csv('./scoresLst.csv',index=False)
# pd.DataFrame(posLst,columns=['Score']).to_csv('./posDist.csv',index=False)
# pd.DataFrame(negLst,columns=['Score']).to_csv('./negDist.csv',index=False)
# pd.DataFrame(mixLst,columns=['Score']).to_csv('./mixDist.csv',index=False)

# coAnnos = []
# nonCoAnnos = []
# for pair in genePairs:
#     if pair[0] in neg or pair[1] in neg:
#         co = False
#         for leaf in leaves:
#             if pair[0] in leaf[1] and pair[1] in leaf[1]:
#                 coAnnos.append(pair[2])
#                 co = True
#                 break
#         if not co:
#             nonCoAnnos.append([pair[2]])

# pd.DataFrame(coAnnos,columns=['Score']).to_csv('./negDist_coAnno.csv',index=False)
# pd.DataFrame(nonCoAnnos,columns=['Score']).to_csv('./negDist_nonCoAnno.csv',index=False)
        
            


# print(len(pos))
# print(len(neg))


print(genePairs)

