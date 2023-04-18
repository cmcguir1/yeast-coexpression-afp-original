
from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph
import sys
from ComplexModel import ComplexModel
import pandas as pd
import torch
from AllGoModel import AllGoModel
from CorrelationDictionary import CorrelationDictionary
import os


# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    if sys.argv[3] == 'T' or sys.argv[3] == 'True':
        calcAll = True
    else:
        calcAll=False
    
    GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()

    start = int(sys.argv[1]) * 10
    if start >= 90:
        r = range(start,len(GoTerms))
    else:
        r = range(start,start+10)
    
    for i in r:
        term = GoTerms[i,0]

        if (os.path.exists(f'./Yeast Resources/Pairwise/Spell/AllSingleTerms/{term[0:2]}{term[3:]}_2000x1_Net_fold1.csv') and 
            os.path.exists(f'./Yeast Resources/Pairwise/Spell/AllSingleTerms/{term[0:2]}{term[3:]}_2000x1_Net_fold2.csv') and 
            os.path.exists(f'./Yeast Resources/Pairwise/Spell/AllSingleTerms/{term[0:2]}{term[3:]}_2000x1_Net_fold3.csv') and 
            os.path.exists(f'./Yeast Resources/Pairwise/Spell/AllSingleTerms/{term[0:2]}{term[3:]}_2000x1_Net_fold4.csv')):


            modelData = PairwiseYeastData(dataset='original',foldFile=f'./Yeast Resources/Datasets/All Spell/_Folds_Original_1.csv',term=term,memMapLoc='../YeastMemMap/YeastCorrDictionary.dat')
            graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/AllSingleTerms/{term[0:2]}{term[3:]}_2000x1_Net_fold',modelData,'113x2000x1',term,'AllSingle_New')
            if sys.argv[2] == 'runAll':
                graph.feedForward(save=False,calcAll=calcAll)
                graph.rankGenes()
                
            else:
                graph.forward(int(sys.argv[2]))


if __name__ == '__main__':
    main()
