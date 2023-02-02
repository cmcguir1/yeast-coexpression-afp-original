
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
    term = sys.argv[1]

    modelData = PairwiseYeastData(dataset='original',foldFile=f'./Yeast Resources/Datasets/All Spell/{term[0:2]}{term[3:]}_Folds_Original_1.csv',term=term,memMapLoc='../YeastMemMap/YeastCorrDictionary.dat')
    model = PairwiseModel(modelData,int(sys.argv[3]),f'{sys.argv[2]}x1','Spell/OtherSingleTerms',f'{term[0:2]}{term[3:]}')
    model.trainNetwork(200000,printLoss=True)
    model.testNetworkTraining(limitNegative=True)
    model.testNetworkValidation(limitNegative=True)



if __name__ == '__main__':
    main()
