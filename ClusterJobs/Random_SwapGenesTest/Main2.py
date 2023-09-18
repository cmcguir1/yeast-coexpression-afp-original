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

    start = time.time()

    
    GOTest = AllGoModel(int(sys.argv[1]),'25000','CE_RandomLabels_swapGenes',f'Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='original',resetNet=False,inputVector='x',outputVector='b',cuda=False,lossFunc='CE',swapGenes=True)
    # GOTest.trainNetwork(100000,track=100,onlyPos=True)
    GOTest.testNetworkAll(runAll=True)
    GOTest.testNetworkAll(runAll=True,validation=False)







if __name__ == '__main__':
    main()

