
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

    #GOTest = AllGoModel(i,sys.argv[1],'AllGO_Original_Parameter','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',ontologyDataset='original',inputDropout=float(sys.argv[2]),hiddenDropout=float(sys.argv[3]))

    # GOTest = AllGoModel(int(sys.argv[2]),sys.argv[1],f'Batch1','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',ontologyDataset='original',batch=1,lr=0.001)
    # GOTest.trainNetwork(1000000)
    # GOTest.testNetworkAll(runAll=True)
    # GOTest.testNetworkAll(runAll=True,validation=False)

    graph = AllGoGraph('./Yeast Resources/Pairwise/Spell/AllGO_Original_Struct\Original_113x25000x92_Net_fold','113x25000x92','Large_SaveAll',ontologyDataset='original')
    graph.feedForward(int(sys.argv[1]),calcPos=True,saveAll=True)
    #graph.feedForward(int(sys.argv[1]),calcAgn=False,saveAll=True)
    #graph.rankGenes()





if __name__ == '__main__':
    main()

