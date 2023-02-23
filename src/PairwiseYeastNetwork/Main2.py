
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
    
    GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
    GOTermDict = {term[1]: term[0] for term in GoTerms}
    for j in range(int(sys.argv[1]),int(sys.argv[1])+4):
        term = GOTermDict[j]

        modelData = PairwiseYeastData(dataset='original',foldFile=f'./Yeast Resources/Datasets/All Spell/{term[0:2]}{term[3:]}_Folds_Original_1.csv',term=term,memMapLoc='../YeastMemMap/YeastCorrDictionary.dat')
        for i in range(4):
            model = PairwiseModel(modelData,i,f'2000x1','Spell/AllrSingleTerms',f'{term[0:2]}{term[3:]}')
            model.trainNetwork(125000,printLoss=True)
            model.testNetworkTraining(limitNegative=True)
            model.testNetworkValidation(limitNegative=True)



if __name__ == '__main__':
    main()
