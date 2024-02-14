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
from ExpressionDatasets import ExpressionDatasets
from AllGOGraph import AllGoGraph
import os
import random

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes
from GOParser import GOParser

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    # model = AllGoModel(0,'100','Test','Test',ontologyDataset='2007',foldFile='./src/PairwiseYeastNetwork/AllGO_2007_b_1.csv',resetNet=True)
    # model.trainNetwork(10000,saveTermLoss=True)

    # graph = AllGoGraph('Test','113x100x79','Debug','Debug',geneFolds='./src/PairwiseYeastNetwork/Test_Folds.csv',ontologyDataset='2007')
    # for i in range(4):
    #     graph.feedForward(i,calcAgn=False,resetScores=i==0)
    # graph.rankGenes(agn=False)

    go = GOParser('2023')
    leaves = go.getSlimLeaves(roots='bcm',onlyLeaves=False)
    data = []
    for id, genes in leaves:
        data.append([id,go.onto.terms[id].name])

    # for id, term in go.onto.terms.items():
    #     data.append([id,term.name])
    pd.DataFrame(data,columns=['GO_id','Name']).to_csv('./src/PairwiseYeastNetwork/GOTerm_names_slim.csv',index=False)

    # for leaf in go.getSlimLeaves():
    #     print(leaf[0],go.onto.terms[leaf[0]].name)
        
    





if __name__ == '__main__':
    main()

