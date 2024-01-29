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

    
    model = AllGoModel(int(sys.argv[1]),'100','HardNegatives','HardNegatives',ontologyDataset='2007',foldFile='src/PairwiseYeastNetwork/AllGO_2007_b_1.csv',resetNet=True)
    model.trainNetwork(100000,hardNegatives=True)
    model.testNetworkAll(hardNegatives=True)
    model.testNetworkAll(validation=False,hardNegatives=True)









if __name__ == '__main__':
    main()

