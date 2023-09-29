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

    

<<<<<<< HEAD
    GOTest = AllGoModel(int(sys.argv[1]),sys.argv[2],'RandomInputs_original','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='original',resetNet=False,inputVector='x',cuda=False,batch=50,memMapName='YeastDict_Random.npy')
=======
    GOTest = AllGoModel(int(sys.argv[1]),'25000','RandomInputs_original','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='original',resetNet=False,inputVector='x',cuda=False,batch=50,memMapName='YeastDict_Random.npy')
>>>>>>> 5ff3177fb48782f38673524226af2c09a7b921c5
    # GOTest.trainNetwork(100000,track=100,onlyPos=True)
    GOTest.testNetworkAll(runAll=True)
    GOTest.testNetworkAll(runAll=True,validation=False)







if __name__ == '__main__':
    main()

