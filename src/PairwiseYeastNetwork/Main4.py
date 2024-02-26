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

    folder = 'Net_bcm'
    name = 'Net_bcm'
    foldFile = './src/PairwiseYeastNetwork/AllGO_2007_bcm_1.csv'

    model = AllGoModel(int(sys.argv[1]),sys.argv[2],folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='bcm',addTerms=[],resetNet=True,hardNegatives=False)
    # model.trainNetwork(500000,saveTermLoss=True)
    # model.testNetworkAll()
    # model.testNetworkAll(validation=False)

    graph = AllGoGraph(model.networkLoc[:-5],f'113x{sys.argv[2]}x118',folder,name,geneFolds=foldFile,outputVector='',addTerms=['GO:0007005'],ontologyDataset='2007',evalDataset='2007')
    graph.feedForward(int(sys.argv[1]),calcAgn=False)
    # graph.rankAllTerms(agn=False)
    # graph.rankGenes(agn=False)


    # graph = AllGoGraph(model.networkLoc[:-5],f'113x{sys.argv[2]}x118',folder,name,geneFolds=foldFile,outputVector='',addTerms=['GO:0007005'],ontologyDataset='2007',evalDataset='2023')
    # graph.feedForward(int(sys.argv[1]),calcAgn=False)
    # graph.rankAllTerms(agn=False,fileSuffix='_Modern')







if __name__ == '__main__':
    main()

