
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
from AllGOGraph import AllGoGraph

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    
    
    folderName = f'Spell/SingleTerm_PS'
    

    terms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary_BioProcOnly.csv').to_numpy()[:,0]
    # term = terms[int(sys.argv[1])]
    term = 'GO:0007005'

    
    for i in range(4):
        model = PairwiseModel(i,f'20x1',folderName,f'{term[0:2]}{term[3:]}_d{sys.argv[2]}_wd{sys.argv[1]}',lr=0.01,resetNet=True,batch=50,term=term,hiddenDrop=float(sys.argv[2]),weightDecay=float(sys.argv[1]))
        model.trainNetwork(10000,printLoss=True)   
        model.testNetworkTraining(limitNegative=True)
        model.testNetworkValidation(limitNegative=True)

    # graph = AllGoGraph(f'Yeast Resources/Pairwise/{folderName}/{term[0:2]}{term[3:]}_{sys.argv[2]}x1_Net_fold',f'113x{sys.argv[2]}x1',f'SingleTerm_{sys.argv[2]}_CorrectFolds',modelName=f'{term[0:2]}{term[3:]}',geneFolds=f'./Yeast Resources/Datasets/All Spell/{term[0:2]}{term[3:]}_Folds_Original_1.csv',ontologyDataset='original',outputVector='',addTerms=[term])
    # graph.feedForward(int(sys.argv[1]),calcAgn=True)
    # graph.rankGenes(term)



if __name__ == '__main__':
    main()
