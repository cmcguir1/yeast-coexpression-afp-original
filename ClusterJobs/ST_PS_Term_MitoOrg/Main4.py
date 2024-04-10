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

    term = sys.argv[1]
    folder = f'ST_L2_Term_PS'
    name = f'{term[0:2]}-{term[3:]}_wd{sys.argv[2]}'
    foldFile = f'./src/PairwiseYeastNetwork/AllGO_2007_{term[0:2]}-{term[3:]}_1.csv'

    # model = AllGoModel(0,'20',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='b',addTerms=[],resetNet=True,hardNegatives=False,weightDecay=float(sys.argv[2]))

    # for i in range(4):
    #     model = AllGoModel(i,'20',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='',addTerms=[term],resetNet=True,hardNegatives=False,weightDecay=float(sys.argv[2]))
    #     model.trainNetwork(200000,saveTermLoss=False)
    #     model.testNetworkAll()
    #     model.testNetworkAll(validation=False)

    model = AllGoModel(0,'20',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='',addTerms=[],resetNet=True,hardNegatives=False,weightDecay=float(sys.argv[2]))

    graph = AllGoGraph(model.networkLoc[:-5],f'113x20x1',folder,name,geneFolds=foldFile,outputVector='',addTerms=[term],ontologyDataset='2007',evalDataset='2023')
    for i in range(4):
        graph.feedForward(i,calcAgn=False,calcPos=True)
    # graph.rankAllTerms(agn=True)
    graph.rankGenes(agn=False,singleTerm=True,term=term)

    # graph = AllGoGraph(model.networkLoc[:-5],f'113x20x1',folder,name,geneFolds=foldFile,outputVector='',addTerms=['GO:0007005'],ontologyDataset='2007',evalDataset='2023')
    # graph.rankGenes(agn=False,singleTerm=True,fileSuffix='_ModernLabelSwap')









if __name__ == '__main__':
    main()

