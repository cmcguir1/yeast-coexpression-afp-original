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

    folder = 'TermSize_Cutoff_Test'
    name = f'Cutoff_{sys.argv[2]}'
    foldFile = f'./src/PairwiseYeastNetwork/AllGO_2007_b_1csv'

   
    model = AllGoModel(int(sys.argv[1]),sys.argv[3],folder,name,foldFile=foldFile,ontologyDataset='2007',expressionDataset='2007',outputVector='b',addTerms=[],resetNet=False,hardNegatives=False,cutoff=int(sys.argv[2]))
    print('Cutoff:',sys.argv[2])
    print('Number of terms:',len(model.leaves))
    model.trainNetwork(600000,saveTermLoss=False)
    model.testNetworkAll()
    model.testNetworkAll(validation=False)

    # model.assessOverfitting()

    netLoc = model.networkLoc[:-5]
    outputSize = len(model.leaves)
    del model
    
    

    graph = AllGoGraph(netLoc,f'{113}x{sys.argv[3]}x{outputSize}',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset='2007',expressionDataset='2007',evalDataset='2023')
    # for i in range(4):
    graph.feedForward(int(sys.argv[1]),calcAgn=True,calcPos=True,flush=True)
    # graph.rankGenes(agn=True,singleTerm=False)
    # graph.rankGenes(agn=True,singleTerm=False,fileSuffix='_Modern',modern=True)
    # graph.rankAllTerms(agn=True,fileSuffix=f'_{onto}_Trained')
    # graph.rankAllTerms(agn=True,fileSuffix=f'_{ontoInverse}_Eval',modern=True)
    



if __name__ == '__main__':
    main()

