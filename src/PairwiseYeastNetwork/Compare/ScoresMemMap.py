import numpy as np
import pandas  as pd
import sys
import time

sys.path.insert(0,'./obopy')
from Leaf import getLeaves

scores = np.memmap('D:/ScoreMemMap.dat',dtype='float32',shape=(27830900,92),mode='r+')
pairs = np.memmap('D:/Pairs.dat',shape=(27830900,2),dtype='U10',mode='r+')

print(scores)
print(pairs)

# print(scores)
# offset = 0
# for i in range(4):
#     print(f"Started Loading fold {i}")
#     data = pd.read_csv(f'D:/posScores_fold{i}.csv').to_numpy()
#     print(f"Loaded fold {i}")
#     scores[offset:offset+len(data),:] = data[:,2:]
#     pairs[offset:offset+len(data),:] = data[:,:2]
#     offset += len(data)
#     del data
# print(f'Length of offset: {offset}')
# print(f'Length of current memmap: {27830900}')
# print(f'Same: {offset == 27830900}\n')




GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
GOTermDict = {term[0]: term[1] for term in GoTerms}

allGenes = pd.read_csv('./src/PairwiseYeastNetwork/AllGOGeneFold1.csv').to_numpy()[:,0]

leaves = getLeaves(10)

for leaf in leaves:
    if leaf[0] == "GO:0007005":
        start = time.time()
        term = leaf[0]
        posSet = leaf[1]
        index = GOTermDict[term]
        print(f'Calculating term {index+1}/92')

        pairsList = []
        posScore = {}
        totalScore = {}

        for gene in allGenes:
            posScore[gene] = 0
            totalScore[gene] = 0
        for i in range(len(pairs)):
            # Calculate Scores
            totalScore[pairs[i,0]] = totalScore[pairs[i,0]] + float(scores[i,index])
            if pairs[i,1] in posSet:
                posScore[pairs[i,0]] = posScore[pairs[i,0]] + float(scores[i,index])

            # Make pairwise list
            if pairs[i,0] in posSet and pairs[i,1] in posSet:
                pairsList.append([1,scores[i,index]])
            else:
                pairsList.append([-1,scores[i,index]])
        singleScores = []
        singleProp = []
        for gene, score in posScore.items():
            if gene in posSet:
                singleScores.append([1,score])
                singleProp.append([1,score/totalScore[gene]])
            else:
                singleScores.append([-1,score])
                singleProp.append([-1,score/totalScore[gene]])
        pd.DataFrame(pairsList,columns=['Label','Score']).to_csv(f'D:/PairScores/{term[0:2]}-{term[3:]}_pairs.csv',index=False)
        pd.DataFrame(singleScores,columns=['Label','Score']).to_csv(f'D:/SingleScores/{term[0:2]}-{term[3:]}_single_pos.csv',index=False)
        pd.DataFrame(singleProp,columns=['Label','Score']).to_csv(f'D:/SingleScores_Prop/{term[0:2]}-{term[3:]}_single_proportion.csv',index=False)
        print(f'Time to calculate: {(time.time()-start)/60} minutes')



