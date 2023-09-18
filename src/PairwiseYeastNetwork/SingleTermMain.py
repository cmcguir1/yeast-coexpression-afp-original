
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
    
    term = sys.argv[1]
    folderName = 'Spell/SingleTerm_lr_0.01'

    
    if sys.argv[4] == 'runAll':
        for i in range(4):
            model = PairwiseModel(i,f'{sys.argv[2]}x1',folderName,f'{term[0:2]}{term[3:]}',lr=float(sys.argv[3]),resetNet=True,batch=50)
            model.trainNetwork(80000,printLoss=True)
            model.testNetworkTraining(limitNegative=True)
            model.testNetworkValidation(limitNegative=True)
    else:
        model = PairwiseModel(int(sys.argv[4]),f'{sys.argv[2]}x1',folderName,f'{term[0:2]}{term[3:]}',batch=50,lr=0.01,resetNet=True)
        model.trainNetwork(100000,printLoss=True)
        model.testNetworkTraining(limitNegative=True)
        model.testNetworkValidation(limitNegative=True)



if __name__ == '__main__':
    main()
