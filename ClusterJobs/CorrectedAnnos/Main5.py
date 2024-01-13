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

    
    # for i in range(0,4):
    # GOTest = AllGoModel(int(sys.argv[2]),sys.argv[1],'CorrectAnnos_Long','BCE',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Original_1.csv',ontologyDataset='original',resetNet=True,verbose='f',lossFunc='BCE')
    # GOTest.trainNetwork(200000,track=100)
    # GOTest.testNetworkAll(runAll=True)
    # GOTest.testNetworkAll(runAll=True,validation=False)

    graph = AllGoGraph(f'./Yeast Resources/Pairwise/Spell/CorrectAnnos_Long/BCE_x_b_113x{sys.argv[1]}x51_lr0.01_batch50_lfBCE_Net_fold',f'113x{sys.argv[1]}x51','BCE_Newfolds','BCE',ontologyDataset='original')
    # graph.feedForward(int(sys.argv[2]))
    graph.rankGenes()







if __name__ == '__main__':
    main()

