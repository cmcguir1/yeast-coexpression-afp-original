
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
from AllGOGraph import AllGoGraph
import os

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    
    graph = AllGoGraph('./Yeast Resources/Pairwise/Spell/AllGO_Original/Original_113x200x92_Net_fold','113x200x92','AllGO_Original',memMapLoc='../YeastMemMap/YeastCorrDictionary.dat')
    graph.feedForward(int(sys.argv[1]))
    #graph.rankGenes()




if __name__ == '__main__':
    main()
