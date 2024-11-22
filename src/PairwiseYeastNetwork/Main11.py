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

    subsetSize = 100000
    start = time.time()

    table = []
    for term, _ in ogModel.getSlimLeaves():
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

        table.append([term, ogModel.onto.terms[term].name,len(ogGenes),np.mean(ogPairs),np.std(ogPairs)])
            
        modPairs = []
        while len(modPairs) < subsetSize:
            geneA = random.choice(modGenes)
            geneB = random.choice(modGenes)
            if geneA != geneB:
                modPairs.append(corrDict.lookupAverageCorrelation(geneA,geneB))

    #     ks = stats.ks_2samp(ogPairs,modPairs)
    #     table.append([term, ogModel.onto.terms[term].name,len(ogGenes),len(modGenes),ks.statistic,ks.pvalue])
    #     print('Time:',time.time()-start)

    pd.DataFrame(table,columns=['Term','Name','Genes','Mean','Std']).to_csv(f'Gene_Correlation_Comparison_subset-{subsetSize}_Simple.csv',index=False)

    # columns = ['Go Term','Name','2007 Genes','2022 Genes','KS Statistic','KS P-Value']
    # pd.DataFrame(table,columns=columns).to_csv(f'Annotation_Correlation_Comparison_subset-{subsetSize}_Simple.csv',index=False)


    








if __name__ == '__main__':
    main()

