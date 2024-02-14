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

    
    # model = AllGoModel(int(sys.argv[1]),sys.argv[2],'Parser_PS','BioProc',foldFile='./src/PairwiseYeastNetwork/AllGO_2007_b_1.csv',ontologyDataset='2007',outputVector='b',resetNet=False)
    # model.trainNetwork(1000000)
    # model.testNetworkAll()
    # model.testNetworkAll(validation=False)

    graph = AllGoGraph(f'./Yeast Resources/Pairwise/Spell/Parser_PS/BioProc_x_b_113x{sys.argv[2]}x79_lr0.01_batch50_lfBCE_Net_fold',f'113x{sys.argv[2]}x79','Parser_PS','BioProc',geneFolds='./src/PairwiseYeastNetwork/AllGO_2007_b_1.csv',outputVector='b',ontologyDataset='2007')
    graph.feedForward(int(sys.argv[1]),calcAgn=False)
    # graph.rankGenes(agn=False)
    # graph.rankAllTerms(agn=False)
    







if __name__ == '__main__':
    main()

