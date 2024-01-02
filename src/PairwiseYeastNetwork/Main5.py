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

    
    for i in range(0,4):
        GOTest = AllGoModel(i,'20','BCE_Paper_Reg_Test','BCE',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='original',resetNet=True,verbose='f',lossFunc='BCE',weightDecay=float(sys.argv[1]),hiddenDropout=float(sys.argv[2]))
        # GOTest.trainNetwork(10000,track=100)
        GOTest.testNetworkAll(runAll=True)
        GOTest.testNetworkAll(runAll=True,validation=False)







if __name__ == '__main__':
    main()

