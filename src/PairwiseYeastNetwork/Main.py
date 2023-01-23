
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

    #Structure Tests

    for i in range(4):
        #GOTest = AllGoModel(i,sys.argv[1],'AllGO_Original_Parameter','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',ontologyDataset='original',inputDropout=float(sys.argv[2]),hiddenDropout=float(sys.argv[3]))
        GOTest = AllGoModel(i,sys.argv[1],'AllGO_Original_Parameter','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',memMapLoc='../YeastMemMap/YeastCorrDictionary.dat',ontologyDataset='original',inputDropout=sys.argv[2],hiddenDropout=sys.argv[3])
        
        GOTest.trainNetwork(10000)
        GOTest.testNetworkAll(runAll=True)
        GOTest.testNetworkAll(runAll=True,validation=False)

    # GO = AllGoModel(0,'200','AllOriginalTest','OriginalDatasets',ontologyDataset='original')
    # GO.trainNetwork(1000)




if __name__ == '__main__':
    main()
