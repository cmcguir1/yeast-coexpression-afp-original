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

    folder = 'Expression_Ontology_Combinations'
    onto = sys.argv[3]
    expr = sys.argv[2]
    name = f'Expr-{expr}_Onto-{onto}'
    foldFile = f'./src/PairwiseYeastNetwork/AllGO_2007_b_1csv'

   
    model = AllGoModel(int(sys.argv[1]),sys.argv[4],folder,name,foldFile=foldFile,ontologyDataset=onto,expressionDataset=expr,outputVector='b',addTerms=[],resetNet=False,hardNegatives=False)
    model.trainNetwork(600000,saveTermLoss=False)
    model.testNetworkAll()
    model.testNetworkAll(validation=False)

    netLoc = model.networkLoc[:-5]
    del model
    

    graph = AllGoGraph(netLoc,f'430x{sys.argv[4]}x93',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset=onto,expressionDataset=expr,evalDataset='2022')
    # for i in range(4):
    graph.feedForward(int(sys.argv[1]),calcAgn=True,calcPos=True,flush=True)
    # graph.rankGenes(agn=True,singleTerm=False)
    # graph.rankGenes(agn=True,singleTerm=False,fileSuffix='_Modern',modern=True)
    # graph.rankAllTerms(agn=True)
    # graph.rankAllTerms(agn=True,fileSuffix='_Modern',modern=True)
    # graph.combineScores()
    # graph.makeGraph()
    # graph.sampleGraph()
    # graph.termSample(folder='MultiTerm_Modern_NetStruct')
    # graph.queryConnections(['VAC14','FAB1','FIG4'])
    # graph.saveSlim()
    # graph.queryConnections(['VAC14','FAB1'])
    # graph.queryConnections(['FIG4'])
    # graph.queryConnections(['SLT2'])
    # graph.queryInvolvement(['VAC14','FAB1','FIG4'])
    # graph.queryInvolvement(['FIG4','STE20'])

    # graph.queryConnections(['FIG4','SLT2'])
    # graph.queryConnections(['FIG4','STE11','STE20'])
    # graph.queryConnections(['FIG4','MEC1'])
    # graph.queryConnections(['FIG4','VMA2','VMA3','VMA5'])
    # graph.queryInvolvement(['FIG4','FAB1','STE20'])
    # graph.normalizeGraph()
    # graph.sampleGraph(folder='MultiTerm_Modern_NetStruct')
    # graph.sampleGraph_PosNeg(folder='MultiTerm_Modern_NetStruct_Labeled')

    # graph.debug()

    

    # graph = AllGoGraph(model.networkLoc[:-5],f'113x{sys.argv[3]}x79',folder,name,geneFolds=foldFile,outputVector='b',addTerms=[],ontologyDataset='2007',evalDataset='2023')
    # graph.rankGenes(agn=False,singleTerm=False,fileSuffix='_Modern')









if __name__ == '__main__':
    main()

