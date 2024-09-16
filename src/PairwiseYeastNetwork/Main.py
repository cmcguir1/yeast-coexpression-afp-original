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
import glob

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes
from GOParser import GOParser

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    name = 'SameFold'
    dataset = 'Test'
    sg = False
    avg = False

    parser = GOParser('2007')
    terms = parser.getSlimLeaves(roots='b')

    slimGenes = set()
    for term, genes in terms:
        slimGenes = slimGenes.union(genes)
    numGenes = len(slimGenes)

    termSize = {}
    for term, genes in terms:
        termSize[term] = len(genes)

    # Pairwise scores
    auc = {}
    pcorp = {}

    for term, genes in terms:
        auc[term] = []
        pcorp[term] = []

    if avg:
        for rep in range(5):
            termAUC = {}
            termPCorp = {}
            for term, genes in terms:
                termAUC[term] = 0
                termPCorp[term] = 0

            for fold in range(4):
                data = pd.read_csv(f'Yeast Resources/Pairwise/Spell/ConsistencyReplicates_{name}/Replicate{rep}_x_b_113x500x200x100x79_lr0.01_batch50_lfBCE_{dataset}_/GOTermDistribution_fold{fold}.csv')
                
                for i, data in data.iterrows():
                    termAUC[data['GO Term']] += data['AUC']
                    randPrec = termSize[data['GO Term']]/numGenes
                    termPCorp[data['GO Term']] += (data['Average Precision'] - randPrec)/ (randPrec)
            for term, genes in terms:
                auc[term].append(termAUC[term]/4)
                pcorp[term].append(termPCorp[term]/4)
            
    else:
        for rep in range(5):
            for fold in range(4):
                data = pd.read_csv(f'Yeast Resources/Pairwise/Spell/ConsistencyReplicates_{name}/Replicate{rep}_x_b_113x500x200x100x79_lr0.01_batch50_lfBCE_{dataset}_/GOTermDistribution_fold{fold}.csv')
                for i, data in data.iterrows():
                    auc[data['GO Term']].append(data['AUC'])
                    randPrec = termSize[data['GO Term']]/numGenes
                    pcorp[data['GO Term']].append((data['Average Precision'] - randPrec)/ (randPrec))



    table = []
    for term, score in auc.items():
        table.append([term, np.mean(score), np.std(score), np.mean(pcorp[term]), np.std(pcorp[term])])

    pd.DataFrame(table,columns=['Term','AUC Mean','AUC Std','PCorp Mean','PCorp Std']).to_csv(f'Yeast Resources/Pairwise/Spell/ConsistencyReplicates_{name}/SummaryStats_{"FoldAverages_" if avg else ""}_{dataset}.csv',index=False)


            



    









if __name__ == '__main__':
    main()

