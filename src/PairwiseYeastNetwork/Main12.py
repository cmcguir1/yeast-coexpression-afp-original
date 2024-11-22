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
import scipy.stats as stats
import random
import time

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes
from GOParser import GOParser

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    ogModel = GOParser('2007')
    modModel = GOParser('2022')

    datasetType = '2022'
    corrDict = CorrelationDictionary(dictLoc=f'../YeastMemMap/YeastDict_Regularized.npy' if (os.path.exists(f'../YeastMemMap/YeastDict_Regularized.npy')) else f'../YeastDict_Regularized.npy',datasetType=datasetType)

    # commonTerms = set([term for term, _ in ogModel.getSlimLeaves()]) & set([term for term, _ in modModel.getSlimLeaves()])

    subsetSize = 200000
    start = time.time()

    slim = ogModel.getSlimLeaves()
    ogGoldStandard = set()
    for term, genes in slim:
        ogGoldStandard.update(genes)

    modernSlim = modModel.getSlimLeaves()
    modern_goldStandard = set()
    for term, genes in modernSlim:
        modern_goldStandard.update(genes)


    ogGoldStandard = list(ogGoldStandard)
    goldStandardPairs = []
    while len(goldStandardPairs) < subsetSize:
        geneA = random.choice(ogGoldStandard)
        geneB = random.choice(ogGoldStandard)
        if geneA != geneB:
            goldStandardPairs.append(corrDict.lookupAverageCorrelation(geneA,geneB,allDatasets=False))

    modern_goldStandard = list(modern_goldStandard)
    modern_goldStandardPairs = []

    while len(modern_goldStandardPairs) < subsetSize:  
        geneA = random.choice(modern_goldStandard)
        geneB = random.choice(modern_goldStandard)
        if geneA != geneB:
            modern_goldStandardPairs.append(corrDict.lookupAverageCorrelation(geneA,geneB,allDatasets=False))

    sharedTerms = list(set([term for term, _ in slim]) & set([term for term, _ in modernSlim]))
   
    list.sort(sharedTerms)
    table = []
    for term in sharedTerms:
        print(term)
        print((time.time()-start)/60)
        ogGenes = list(ogModel.getGenes(term))
        modGenes = list(modModel.getGenes(term))

        
        
        
        
        ogPairs = []
        while len(ogPairs) < subsetSize:
            geneA = random.choice(ogGenes)
            geneB = random.choice(ogGenes)
            if geneA != geneB:
                ogPairs.append(corrDict.lookupAverageCorrelation(geneA,geneB,allDatasets=False))

        modPairs = []
        while len(modPairs) < subsetSize:
            geneA = random.choice(modGenes)
            geneB = random.choice(modGenes)
            if geneA != geneB:
                modPairs.append(corrDict.lookupAverageCorrelation(geneA,geneB))

        

        o_ks = stats.ks_2samp(ogPairs,goldStandardPairs)
        o_bm = stats.brunnermunzel(ogPairs,goldStandardPairs)
        o_e = stats.energy_distance(ogPairs,goldStandardPairs)

        m_ks = stats.ks_2samp(modPairs,modern_goldStandardPairs)
        m_bm = stats.brunnermunzel(modPairs,modern_goldStandardPairs)
        m_e = stats.energy_distance(modPairs,modern_goldStandardPairs)

        table.append([term, ogModel.onto.terms[term].name,len(ogGenes),len(modGenes),o_ks.statistic,o_ks.pvalue,o_bm.statistic,o_bm.pvalue,o_e,m_ks.statistic,m_ks.pvalue,m_bm.statistic,m_bm.pvalue,m_e])
    #     print('Time:',time.time()-start)

    pd.DataFrame(table,columns=['Term','Name','2007 Genes','2022 Genes','KS Stat 2007','KS P-value 2007','BM Stat 2007','BM P-value 2007','Energy Distance 2007','KS Stat 2022','KS P-value 2022','BM Stat 2022','BM P-value 2022','Energy Distance 2022']).to_csv(f'Gene_Correlation_ComparisonToBackground_og-vs-mod_subset-{subsetSize}_dataset-{datasetType}.csv',index=False)

    # columns = ['Go Term','Name','2007 Genes','2022 Genes','KS Statistic','KS P-Value']
    # pd.DataFrame(table,columns=columns).to_csv(f'Annotation_Correlation_Comparison_subset-{subsetSize}_Simple.csv',index=False)


    








if __name__ == '__main__':
    main()

