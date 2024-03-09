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

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes
from GOParser import GOParser

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    parser = GOParser('2007')
    leaves = parser.getSlimLeaves(roots='b')
    term, genes = leaves[int(sys.argv[1])]

    folder = 'SingleTerm_2.28'
    name = f'{term[0:2]}{term[3:]}'
    foldFile = f'./src/PairwiseYeastNetwork/Folds/AllGO_2007_{name}_1.csv'

    model = AllGoModel(0,'5',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='b',addTerms=[],resetNet=True,hardNegatives=False)
    for i in range(0,4):
        model = AllGoModel(i,'5',folder,name,foldFile=foldFile,ontologyDataset='2007',outputVector='',addTerms=[term],resetNet=True,hardNegatives=False)
        model.trainNetwork(100000,saveTermLoss=True)
        model.testNetworkAll()
        model.testNetworkAll(validation=False)

    graph = AllGoGraph(model.networkLoc[:-5],f'113x{sys.argv[2]}x1',folder,name,geneFolds=foldFile,outputVector='',addTerms=[term],ontologyDataset='2007')
    for i in range(0,4):
        graph.feedForward(i,calcAgn=False)
    # graph.rankAllTerms(agn=False)
    # graph.rankGenes(agn=False,singleTerm=True)

    # graph = AllGoGraph(model.networkLoc[:-5],f'113x{sys.argv[2]}x1',folder,name,geneFolds=foldFile,outputVector='',addTerms=[term],ontologyDataset='2007',evalDataset='2023')
    # graph.rankGenes(agn=False,singleTerm=True,fileSuffix='_Modern')







if __name__ == '__main__':
    main()

