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

    #GOTest = AllGoModel(i,sys.argv[1],'AllGO_Original_Parameter','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',ontologyDataset='original',inputDropout=float(sys.argv[2]),hiddenDropout=float(sys.argv[3]))
    start = time.time()
    GOTest = AllGoModel(int(sys.argv[1]),'25000x5000x5000x1000','Modern_LargeStruct',f'Dropout_{sys.argv[2]}',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='modern',lossFunc='CE',hiddenDropout=float(sys.argv[2]),resetNet=True)
    GOTest.trainNetwork(250000,track=100)
    GOTest.testNetworkAll(runAll=True)
    GOTest.testNetworkAll(runAll=True,validation=False)





if __name__ == '__main__':
    main()

