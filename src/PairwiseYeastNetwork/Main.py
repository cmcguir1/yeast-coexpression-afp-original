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
    #     GOTest = AllGoModel(i,sys.argv[1],'BCE_Paper','BCE',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='original',resetNet=True,verbose='f',lossFunc='BCE')
    #     GOTest.trainNetwork(25000,track=100)
    #     GOTest.testNetworkAll(runAll=True)
    #     GOTest.testNetworkAll(runAll=True,validation=False)

    graph = AllGoGraph(f'./Yeast Resources/Pairwise/Spell/BCE_Paper/BCE_x_b_113x{sys.argv[1]}x53_lr0.01_batch50_lfBCE_Net_fold',f'113x{sys.argv[1]}x53','BCE_Paper','BCE',ontologyDataset='original')
    graph.feedForward(int(sys.argv[2]))







if __name__ == '__main__':
    main()

