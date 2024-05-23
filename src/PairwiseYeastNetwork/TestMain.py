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

    folder = 'Test_2'
    name = f'Test'
    foldFile = './src/PairwiseYeastNetwork/AllGO_2007_GO-0007005_1.csv'

   
    model = AllGoModel(0,'20',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='b',addTerms=[],resetNet=False,hardNegatives=False)
    # model.trainNetwork(600000,saveTermLoss=False)
    # model.testNetworkAll()
    # model.testNetworkAll(validation=False)

    graph = AllGoGraph(model.networkLoc[:-5],f'113x20x79',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset='2007',evalDataset='2023')
    # for i in range(4):
    # graph.feedForward(1,calcAgn=True,calcPos=True)
    # graph.feedForward(2,calcAgn=True,calcPos=True)
    # graph.feedForward(3,calcAgn=True,calcPos=True)
    graph.rankGenes(agn=True,singleTerm=False)
    # graph.rankAllTerms(agn=True)
    # graph.debug()

    

    # graph = AllGoGraph(model.networkLoc[:-5],f'113x{sys.argv[3]}x79',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset='2007',evalDataset='2023')
    # graph.rankGenes(agn=False,singleTerm=False,fileSuffix='_Modern')









if __name__ == '__main__':
    main()

