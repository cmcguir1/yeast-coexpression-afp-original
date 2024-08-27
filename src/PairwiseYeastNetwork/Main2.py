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
from AllGOGraph import AllGoGraph

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    folder = 'MultiTerm_NetStruct_PS'
    name = f'Replicate_0_'
    foldFile = f'./src/PairwiseYeastNetwork/AllGO_2007_GO-0007005_0.csv'

   
    # model = AllGoModel(0,'500x200x100',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='b',addTerms=[],resetNet=False,hardNegatives=False)
    # model.trainNetwork(600000,saveTermLoss=False)
    # model.testNetworkAll()
    # model.testNetworkAll(validation=False)

    graph = AllGoGraph('./Yeast Resources/Pairwise/Spell/MultiTerm_NetStruct_PS/Replicate_0__x_b_113x500x200x100x79_lr0.01_batch50_lfBCE_Net_fold',f'113x500x200x100x79',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset='2007',evalDataset='2023')
    # for i in range(4):
    # graph.feedForward(int(sys.argv[1]),calcAgn=True,calcPos=True,flush=True)
    # graph.rankGenes(agn=True,singleTerm=False)
    # graph.rankGenes(agn=True,singleTerm=False,fileSuffix='_Modern',modern=True)
    # graph.rankAllTerms(agn=True)
    # graph.rankAllTerms(agn=True,fileSuffix='_Modern',modern=True)
    
    # graph.combineScores()
    # graph.makeGraph()
    # graph.sampleGraph()
    # graph.termSample(folder=folder)
    # graph.sampleGraph(folder=folder)
    graph.sampleGraph_PosNeg(folder='MultiTerm_NetStruct_PS_Labeled')

    # graph.debug()

    

    # graph = AllGoGraph(model.networkLoc[:-5],f'113x{sys.argv[3]}x79',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset='2007',evalDataset='2023')
    # graph.rankGenes(agn=False,singleTerm=False,fileSuffix='_Modern')









if __name__ == '__main__':
    main()

