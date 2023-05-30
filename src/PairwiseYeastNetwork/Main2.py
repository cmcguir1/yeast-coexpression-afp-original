
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
from MemMapGraph import MemMapGraph
from AllGOGraph import AllGoGraph
import os

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    # graph = MemMapGraph('./AllScoreMemMap.dat','MemMap_Original_113x2000x92')
    # graph.rankTerm('GO:0007005')
    
    # modelData = PairwiseYeastData(dataset='original',foldFile=f'./Yeast Resources/Datasets/All Spell/GO-0007005_Folds_Original_1.csv',term='GO:0007005',memMapLoc='../YeastMemMap/YeastCorrDictionary.dat')
    # graph = YeastGraph('./Yeast Resources/Pairwise/Spell/AllSingleTerms/GO0007005_2000x1_Net_fold',modelData,'113x2000x1','GO:0007005','AllSingle_New')
    # graph.rankPos()

    # GOTest = AllGoModel(int(sys.argv[1]),sys.argv[2],f'BioProcessOnly',f'BioProcessOnly',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv',ontologyDataset='original',resetNet=True,cuda=False,onlyBioProc=True)
    # GOTest.trainNetwork(80000,track=100)
    # GOTest.testNetworkAll(runAll=True)
    # GOTest.testNetworkAll(runAll=True,validation=False)

    graph = AllGoGraph(f'./Yeast Resources/Pairwise/Spell/bioPIXIE_Data/Original_149x{sys.argv[2]}x53_Net_fold',f'149x{sys.argv[2]}x53','bioPIXIE_Data',inputVector='xlgp',ontologyDataset='original')
    # graph.feedForward(int(sys.argv[1]),saveAll=True,runBatch=True)
    graph.rankGenes()
    



if __name__ == '__main__':
    main()
