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
    batch = int(sys.argv[1])
    
    for i in range(0,4):
        GOTest = AllGoModel(i,'100','Batch_PS',f'Folds{sys.argv[2]}',foldFile=f'./src/PairwiseYeastNetwork/AllGO_2007_b_{sys.argv[2]}.csv',ontologyDataset='original',resetNet=True,verbose='f',lossFunc='BCE',batch=batch,resetNet=True)
        GOTest.trainNetwork(100000,track=100)
        GOTest.testNetworkAll(runAll=True)
        GOTest.testNetworkAll(runAll=True,validation=False)

    







if __name__ == '__main__':
    main()

