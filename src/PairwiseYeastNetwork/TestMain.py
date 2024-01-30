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
from ExpressionDatasets import ExpressionDatasets
from AllGOGraph import AllGoGraph
import os
import random

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    graph = AllGoGraph('Test','113x100x79','Debug','Debug',geneFolds='./src/PairwiseYeastNetwork/Test_Folds.csv',ontologyDataset='2007')
    for i in range(4):
        graph.feedForward(i,calcAgn=False,resetScores=i==0)
    graph.rankGenes(agn=False)
    





if __name__ == '__main__':
    main()

