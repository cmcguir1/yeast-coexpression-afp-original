
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
    
    
    folderName = f'Spell/SingleTerm_{sys.argv[2]}'

    terms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary_BioProcOnly.csv').to_numpy()[:,0]
    term = terms[int(sys.argv[1])]

    
    
    # for i in range(4):
        # model = PairwiseModel(i,f'{sys.argv[2]}x1',folderName,f'{term[0:2]}{term[3:]}',lr=0.01,resetNet=True,batch=50)
        # model.trainNetwork(20000,printLoss=True)
        # model.testNetworkTraining(limitNegative=True)
        # model.testNetworkValidation(limitNegative=True)
    graph = YeastGraph(f'GO0000054_{sys.argv[2]}x1_Net_fold',f'113x{sys.argv[2]}',term,f'SingleTerms_{sys.argv[2]}')
    graph.feedForward(save=False,calcAll=True,calcAgn=True)
    graph.recombineFolds()
    graph.rankGenes()



if __name__ == '__main__':
    main()
