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

    
    
    graph = AllGoGraph(f'./Yeast Resources/Pairwise/Spell/HeterogeneousData_Opt/Heterogeneous_Reg_BCE_glpx_b_149x20x53_lr0.01_batch50_wd0.005_lfBCE_hiddenDrop0.5_Net_fold',f'149x20x53','Heterogeneous_Reg_BCE_20',ontologyDataset='original',inputVector='xlgp')
    # graph.rankGenes()
    # graph.feedForward(int(sys.argv[1]),saveAll=True,runBatch=True,calcPos=True)
    graph.rankAllTerms()







if __name__ == '__main__':
    main()

