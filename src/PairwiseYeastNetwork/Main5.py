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

    folder = 'ST_MitoOrg_L2'
    name = f'MitoOrg_wd{sys.argv[2]}'
    foldFile = './src/PairwiseYeastNetwork/AllGO_2007_GO-0007005_1.csv'

    model = AllGoModel(int(sys.argv[1]),'20',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='',addTerms=['GO:0007005'],resetNet=True,hardNegatives=False,weightDecay=float(sys.argv[2]))
    # model.trainNetwork(100000,saveTermLoss=True)
    # model.testNetworkAll()
    # model.testNetworkAll(validation=False)

    # graph = AllGoGraph(model.networkLoc[:-5],f'113x20x1',folder,name,geneFolds=foldFile,outputVector='',addTerms=['GO:0007005'],ontologyDataset='2007')
    # graph.feedForward(int(sys.argv[1]),calcAgn=True,calcPos=False)
    # graph.rankAllTerms(agn=True)
    # graph.rankGenes(agn=True,singleTerm=True)

    graph = AllGoGraph(model.networkLoc[:-5],f'113x20x1',folder,name,geneFolds=foldFile,outputVector='',addTerms=['GO:0007005'],ontologyDataset='2007',evalDataset='2023')
    graph.rankGenes(agn=False,singleTerm=True,fileSuffix='_ModernLabelSwap')









if __name__ == '__main__':
    main()

