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

    
    # model = AllGoModel(int(sys.argv[1]),'100','HardNegatives','HardNegatives_Redo',ontologyDataset='2007',foldFile='src/PairwiseYeastNetwork/AllGO_2007_b_1.csv',resetNet=True)
    # model.trainNetwork(100000,hardNegatives=True)
    # model.testNetworkAll(hardNegatives=True)
    # model.testNetworkAll(validation=False,hardNegatives=True)

    graph = AllGoGraph('Yeast Resources/Pairwise/Spell/HardNegatives_Redo/HardNegatives_x_b_113x100x79_lr0.01_batch50_lfBCE_Net_fold','113x100x79','HardNegatives','HardNegatives',geneFolds='src/PairwiseYeastNetwork/AllGO_2007_b_1.csv',ontologyDataset='2007',outputVector='b')
    graph.feedForward(int(sys.argv[1]),calcAgn=False)
    # graph.rankGenes(agn=False)









if __name__ == '__main__':
    main()

