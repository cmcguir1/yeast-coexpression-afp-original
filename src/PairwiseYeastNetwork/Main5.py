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
    term = 'GO:0007005'
    #GOTest = AllGoModel(i,sys.argv[1],'AllGO_Original_Parameter','Original',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',ontologyDataset='original',inputDropout=float(sys.argv[2]),hiddenDropout=float(sys.argv[3]))
    modelData = PairwiseYeastData(dataset='original',foldFile=f'./Yeast Resources/Datasets/All Spell/_Folds_Original_1.csv',term='GO:0007005',memMapLoc='../YeastMemMap/YeastCorrDictionary.dat')
    graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/SingleTerm_lr_0.01/{term[0:2]}{term[3:]}_2000x1_Net_fold',modelData,'113x2000x1',term,'MitoOrg_ST')
    graph.forward(int(sys.argv[1]),calcAll=True,track=1000,batchSize=1000,calcAgn=True)





if __name__ == '__main__':
    main()

