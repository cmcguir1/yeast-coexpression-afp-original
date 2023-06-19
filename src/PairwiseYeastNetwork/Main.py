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

    if sys.argv[2] == 'YeastDict_ReCalc.npy':
        name = 'ReCalc'
    else:
        name = 'Original'

    GOTest = AllGoModel(int(sys.argv[1]),'2000','Test_MemMap_ReCalc2',name,foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='original',resetNet=True,inputVector='x',cuda=False,batch=50,memMapName=sys.argv[2])
    GOTest.trainNetwork(40000,track=100)
    GOTest.testNetworkAll(runAll=True)
    GOTest.testNetworkAll(runAll=True,validation=False)







if __name__ == '__main__':
    main()

