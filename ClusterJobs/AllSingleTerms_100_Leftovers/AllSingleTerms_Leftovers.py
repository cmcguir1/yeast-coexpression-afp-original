
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

    
    terms = ['GO:0006310', 'GO:0006325', 'GO:0006352', 'GO:0007005', 'GO:0008643', 'GO:0009408', 'GO:0009451', 'GO:0016197', 'GO:0032196', 'GO:0032543', 'GO:0042273', 'GO:0042274', 'GO:0051321', 'GO:0051603', 'GO:0051726']
    term = terms[int(sys.argv[1])]
    
    
    for i in range(4):
        model = PairwiseModel(i,f'{sys.argv[2]}x1',folderName,f'{term[0:2]}{term[3:]}',lr=0.01,resetNet=True,batch=50)
        model.trainNetwork(20000,printLoss=True)
        model.testNetworkTraining(limitNegative=True)
        model.testNetworkValidation(limitNegative=True)
    graph = YeastGraph(f'Yeast Resources/Pairwise/Spell/SingleTerm_{sys.argv[2]}/{term[0:2]}{term[3:]}_{sys.argv[2]}x1_Net_fold',f'113x{sys.argv[2]}x1',term,f'SingleTerms_{sys.argv[2]}')
    graph.feedForward(save=False,calcAll=True,calcAgn=True,calcPos=True)
    graph.recombineFolds(agn=True)
    graph.rankGenes()



if __name__ == '__main__':
    main()
