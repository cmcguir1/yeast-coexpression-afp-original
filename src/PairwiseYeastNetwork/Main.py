
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



    GOTest = AllGoModel(int(sys.argv[1]),sys.argv[2],f'MassiveNetwork',f'Dropout_{sys.argv[3]}',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',ontologyDataset=sys.argv[4],batch=50,resetNet=True,hiddenDropout=float(sys.argv[3]))
    GOTest.trainNetwork(100000,track=100)
    GOTest.testNetworkAll(runAll=True)
    GOTest.testNetworkAll(runAll=True,validation=False)
    



if __name__ == '__main__':
    main()
