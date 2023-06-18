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

    start = int(sys.argv[1]) * 27
    end = start + 27
    if end > 430:
        end = 430

    corr = CorrelationDictionary(dictLoc='../YeastMemMap/YeastDict.dat')
    for dataset in corr.datasets[start:end]:
        corr.calculateDataset(corr.datasetsDict[dataset],location=f'../YeastMemMap_ReCalc/{dataset}_correlations.npy')
    






if __name__ == '__main__':
    main()

