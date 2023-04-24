import pandas as pd
import numpy as np
import glob
import os
import sys
import time

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

def score(memmapLoc='./AllScoreMemMap.dat',includeAgn=True,dir=''):
    scores = np.memmap(memmapLoc,dtype='float32',shape=(27830900+5850565,92),mode='r+')
    pairs = np.memmap('./AllPairs.dat',shape=(27830900+5850565,2),dtype='U10',mode='r+')

    bioProc = set(getGenes('GO:0008150'))

    print(scores)
    print(pairs)




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
        mitoIndex = GOTermDict['GO:0007005']


        print(f'Calculating term {index+1}/92')

        pairsList = []

        for i in pairRange:
            # Make pairwise list
            if pairs[i,1] in posSet:
                if pairs[i,0] in posSet:
                    pairsList.append([1,scores[i,index]])
                elif pairs[i,0] in negSet:
                    pairsList.append([-1,scores[i,index]])

        if(not os.path.exists(f'D:{dir}')):
            os.mkdir(f'D:{dir}')
        if(not os.path.exists(f'D:{dir}/PairScores')):
            os.mkdir(f'D:{dir}/PairScores')

        
        pd.DataFrame(pairsList,columns=['Label','Score']).to_csv(f'D:{dir}/PairScores/{term[0:2]}-{term[3:]}_pairs.csv',index=False)
        print(f'Time to calculate term {index+1}/92 : {(start-time.time())/60}')


score(includeAgn=False,dir='/OnlyPos')


