import numpy as np
import pandas  as pd
import sys
import time
import os

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

def score(memmapLoc='./AllScoreMemMap.dat',includeAgn=True,dir=''):
    scores = np.memmap(memmapLoc,dtype='float32',shape=(27830900+5850565,92),mode='r+')
    pairs = np.memmap('./AllPairs.dat',shape=(27830900+5850565,2),dtype='U10',mode='r+')

    bioProc = set(getGenes('GO:0008150'))

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
    if includeAgn:
        pairRange = range(len(pairs))
    else:
        pairRange = range(27830900)

    for leaf in leaves:
        start = time.time()
        term = leaf[0]
        posSet = leaf[1]
        negSet = set()
        for l in leaves:
            if l[0] != leaf[0]:
                negSet = negSet | l[1]
        agnSet = (bioProc - negSet) - posSet

        index = GOTermDict[term]


        print(f'Calculating term {index+1}/92')

        pairsList = []
        posScore = {}
        posScore_num = {}
        totalScore = {}
        totalScore_num = {}

        for gene in allGenes:
            posScore[gene] = 0
            posScore_num[gene] = 0
            totalScore[gene] = 0
            totalScore_num[gene] = 0
        for i in pairRange:
            # Calculate Scores
            totalScore[pairs[i,0]] = totalScore[pairs[i,0]] + float(scores[i,index])
            totalScore_num[pairs[i,0]] = totalScore_num[pairs[i,0]] + 1
            if pairs[i,1] in posSet:
                posScore[pairs[i,0]] = posScore[pairs[i,0]] + float(scores[i,index])
                posScore_num[pairs[i,0]] = posScore_num[pairs[i,0]] + 1

            # Make pairwise list
            if pairs[i,0] in posSet and pairs[i,1] in posSet:
                pairsList.append([1,scores[i,index]])
            elif (not (pairs[i,0] in agnSet)) and (not (pairs[i,1] in agnSet)):
                pairsList.append([-1,scores[i,index]])
            else:
                pairsList.append([0,scores[i,index]])
        singleScores = []
        totalScoreLst = []
        singleProp = []
        
        for gene, score in posScore.items():
            if gene in posSet:
                label = 1
            elif gene in negSet:
                label = -1
            else:
                label = 0
            singleScores.append([label,score/posScore_num[gene]])
            totalScoreLst.append([label,totalScore[gene]/totalScore_num[gene]])
            singleProp.append([label,score/totalScore[gene]])

        if(not os.path.exists(f'D:{dir}')):
            os.mkdir(f'D:{dir}')
        if(not os.path.exists(f'D:{dir}/SingleScores_Pos')):
            os.mkdir(f'D:{dir}/SingleScores_Pos')
        if(not os.path.exists(f'D:{dir}/SingleScores_Prop')):
            os.mkdir(f'D:{dir}/SingleScores_Prop')
        if(not os.path.exists(f'D:{dir}/SingleScores_Background')):
            os.mkdir(f'D:{dir}/SingleScores_Background')
        if(not os.path.exists(f'D:{dir}/PairScores')):
            os.mkdir(f'D:{dir}/PairScores')
        
        pd.DataFrame(pairsList,columns=['Label','Score']).to_csv(f'D:{dir}/PairScores/{term[0:2]}-{term[3:]}_pairs.csv',index=False)
        pd.DataFrame(singleScores,columns=['Label','Score']).to_csv(f'D:{dir}/SingleScores_Pos/{term[0:2]}-{term[3:]}_single_pos.csv',index=False)
        pd.DataFrame(singleProp,columns=['Label','Score']).to_csv(f'D:{dir}/SingleScores_Prop/{term[0:2]}-{term[3:]}_single_proportion.csv',index=False)
        pd.DataFrame(totalScoreLst,columns=['Label','Score']).to_csv(f'D:{dir}/SingleScores_Background/{term[0:2]}-{term[3:]}_single_background.csv',index=False)
        print(f'Time to calculate: {(time.time()-start)/60} minutes')


score(includeAgn=False,dir='/Background')


