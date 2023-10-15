from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph
from AllGOGraph import AllGoGraph
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

    
    
    graph = AllGoGraph(f'./Yeast Resources/Pairwise/Spell/Opt_Dropout+WD/Original_x_b_113x20x53_lr0.01_batch50_wd0.0025_hiddenDrop0.1_Net_fold',f'113x20x53','Opt_Net20_WD0.0025_Dropout0.1',ontologyDataset='original',inputVector='x')
    # graph.rankGenes()
    graph.feedForward(int(sys.argv[1]),saveAll=True,runBatch=True)







if __name__ == '__main__':
    main()

