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

    
    # model = AllGoModel(int(sys.argv[1]),'100','Parser','AllRoots_nonLeaves',foldFile='./src/PairwiseYeastNetwork/AllGO_2007_bcml_1.csv',ontologyDataset='2007',outputVector='bcml',resetNet=False)
    # model.trainNetwork(200000)
    # model.testNetworkAll()
    # model.testNetworkAll(validation=False)

    graph = AllGoGraph('./Yeast Resources/Pairwise/Spell/Parser/AllRoots_nonLeaves_x_bclm_113x100x140_lr0.01_batch50_lfBCE_Net_fold','113x100x140','Parser','AllRoots+nonLeaves',geneFolds='./src/PairwiseYeastNetwork/AllGO_2007_bcml_1.csv',outputVector='bcml',ontologyDataset='2007')
    # graph.feedForward(int(sys.argv[1]),calcAgn=False)
    graph.rankGenes(agn=False)







if __name__ == '__main__':
    main()

