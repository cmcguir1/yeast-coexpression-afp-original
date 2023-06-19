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


    corr = CorrelationDictionary(dictLoc='../YeastMemMap/YeastDict_float16.npy')
    corr.unifyCorrelations('../YeastMemMap_ReCalc/YeastDict_ReCalc2.npy')
    

    






if __name__ == '__main__':
    main()

