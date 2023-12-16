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
import os
import random

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    corr = CorrelationDictionary(dictLoc='../YeastDict_Regularized.npy',datasetType='original')
    
        
    
    ontDataset = 'original'
    mitoOrg = getGenes('GO:0007005',dataset=ontDataset)
    mitoTrans = getGenes('GO:0032543',dataset=ontDataset)
    bioProc = getGenes('GO:0008150',dataset=ontDataset)
    # print(f'Mitochondrial Organization Genes: {len(mitoOrg)}')
    # print(f'Translation Genes: {len(translation)}')
    # print(f'Mitochondrial Translation genes: {len(mitoTrans)}')
    # print(f'MitoOrg and Translation: {len(mitoOrg & translation)}')
    # print(f'MitoOrg and MitoTrans: {len(mitoOrg & mitoTrans)}')
    # print(f'MitoTrans and Translation: {len(mitoTrans & translation)}')

    org_org = [(mitoOrg[i],mitoOrg[j]) for i in range(len(mitoOrg)) for j in range(i+1,len(mitoOrg))]
    org_trans = [(mitoOrg[i],mitoTrans[j]) for i in range(len(mitoOrg)) for j in range(0,len(mitoTrans))]
    trans_trans = [(mitoTrans[i],mitoTrans[j]) for i in range(len(mitoTrans)) for j in range(i+1,len(mitoTrans))]
    background = [(bioProc[i],bioProc[j]) for i in range(len(bioProc)) for j in range(len(bioProc)) if i != j]
    random.shuffle(background)
    background = background[:len(org_org)]

    org_org_table = np.ndarray((len(org_org),len(corr.datasets)))
    org_trans_table = np.ndarray((len(org_trans),len(corr.datasets)))
    trans_trans_table = np.ndarray((len(trans_trans),len(corr.datasets)))
    background_table = np.ndarray((len(background),len(corr.datasets)))

    pd.DataFrame(org_org_table,columns=corr.datasets).to_csv('D:/CorrelationComparison_org_org.csv',index=False)
    pd.DataFrame(org_trans_table,columns=corr.datasets).to_csv('D:/CorrelationComparison_org_trans.csv',index=False)
    for i,(geneA, geneB) in enumerate(org_org):
        for j in range(len(corr.datasets)):
            org_org_table[i,j] = corr.lookupCorrelation(geneA,geneB,corr.datasets[j])
    for i,(geneA, geneB) in enumerate(org_trans):
        for j in range(len(corr.datasets)):
            org_trans_table[i,j] = corr.lookupCorrelation(geneA,geneB,corr.datasets[j])

    for i,(geneA, geneB) in enumerate(trans_trans):
        for j in range(len(corr.datasets)):
            trans_trans_table[i,j] = corr.lookupCorrelation(geneA,geneB,corr.datasets[j])
    for i,(geneA, geneB) in enumerate(background):
        for j in range(len(corr.datasets)):
            background_table[i,j] = corr.lookupCorrelation(geneA,geneB,corr.datasets[j])


    pd.DataFrame(org_org_table,columns=corr.datasets).to_csv('D:/CorrelationComparison_org_org.csv',index=False)
    pd.DataFrame(org_trans_table,columns=corr.datasets).to_csv('D:/CorrelationComparison_org_trans.csv',index=False)
    pd.DataFrame(trans_trans_table,columns=corr.datasets).to_csv('D:/CorrelationComparison_trans_trans.csv',index=False)
    pd.DataFrame(background_table,columns=corr.datasets).to_csv('D:/CorrelationComparison_background.csv',index=False)

        

    





if __name__ == '__main__':
    main()

