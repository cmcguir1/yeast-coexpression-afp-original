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
    corr = CorrelationDictionary(dictLoc='../YeastMemMap/YeastDict.dat')
    for dataset in corr.datasets[start:end]:
        corr.calculateDataset(corr.datasetsDict[dataset],location=f'../YeastMemMap_ReCalc/{dataset}_correlations.npy')
=======
    corr = CorrelationDictionary(dictLoc='../YeastDict_float16.npy')
    corr.unifyCorrelations('../YeastMemMap_ReCalc/YeastDict_ReCalc.npy')
    
>>>>>>> 75d8b038a21a9bf59e83bf975905182f88cb0847
    






if __name__ == '__main__':
    main()

