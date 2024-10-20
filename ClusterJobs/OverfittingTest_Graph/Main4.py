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

    folder = 'OverfittingTest'
    name = f'Batches_{sys.argv[3]}'
    foldFile = f'./src/PairwiseYeastNetwork/AllGO_2007_b_1csv'

   
    model = AllGoModel(int(sys.argv[1]),sys.argv[2],folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='b',addTerms=[],resetNet=False,hardNegatives=False)
    # model.trainNetwork(int(sys.argv[3]),saveTermLoss=False)
    # model.testNetworkAll()
    # model.testNetworkAll(validation=False)
    model.assessOverfitting()
    netLoc = model.networkLoc[:-5]
    del model

    graph = AllGoGraph(netLoc,f'113x{sys.argv[2]}x79',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset='2007',evalDataset='2023')
    # for i in range(4):
    graph.feedForward(int(sys.argv[1]),calcAgn=True,calcPos=True,flush=True)
    # graph.rankGenes(agn=True,singleTerm=False)
    # graph.rankGenes(agn=True,singleTerm=False,fileSuffix='_Modern',modern=True)
    graph.rankAllTerms(agn=True)
    graph.rankAllTerms(agn=True,fileSuffix='_Modern',modern=True)









if __name__ == '__main__':
    main()

