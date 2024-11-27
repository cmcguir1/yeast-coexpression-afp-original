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
    # ogModel = GOParser('2007')
    # modModel = GOParser('2022')

    corrDict = CorrelationDictionary(dictLoc=f'../YeastMemMap/YeastDict_Regularized.npy' if (os.path.exists(f'../YeastMemMap/YeastDict_Regularized.npy')) else f'../YeastDict_Regularized.npy',datasetType='2022')

    print('Total Exp Conditions:', corrDict.totalExperimetnalConditions())

    # commonTerms = set([term for term, _ in ogModel.getSlimLeaves()]) & set([term for term, _ in modModel.getSlimLeaves()])

    # subsetSize = 10000
    # start = time.time()

    # table = []
    # for term in commonTerms - set(['GO:0006360']):
    #     print(term)
    #     ogGenes = ogModel.getGenes(term)
    #     modGenes = modModel.getGenes(term)
    #     N = list(modGenes - ogGenes) # Genes newly annotated from 2007 to 2022
    #     C = list(modGenes & ogGenes) # Genes consistently annotated in both 2007 and 2022
    #     M = list(ogGenes - modGenes) # Genes removed from 2007 to 2022
    #     NxN = [corrDict.lookupAverageCorrelation(random.choice(N),random.choice(N)) for _ in range(subsetSize)]
    #     CxC = [corrDict.lookupAverageCorrelation(random.choice(C),random.choice(C)) for _ in range(subsetSize)]
    #     MxM = [corrDict.lookupAverageCorrelation(random.choice(M),random.choice(M)) for _ in range(subsetSize)]
    #     NxC = [corrDict.lookupAverageCorrelation(random.choice(N),random.choice(C)) for _ in range(subsetSize)]
    #     NxM = [corrDict.lookupAverageCorrelation(random.choice(N),random.choice(M)) for _ in range(subsetSize)]
    #     CxM = [corrDict.lookupAverageCorrelation(random.choice(C),random.choice(M)) for _ in range(subsetSize)]
    #     print('Time:',time.time()-start)
    #     start = time.time()

    #     row  = [term, ogModel.onto.terms[term].name,len(ogGenes),len(modGenes),len(N),len(C),len(M),np.mean(NxN),np.mean(CxC),np.mean(MxM),np.mean(NxC),np.mean(NxM),np.mean(CxM)]

    #     ks_CxC_CxM = stats.ks_2samp(CxC,CxM)
    #     ks_MxM_CxM = stats.ks_2samp(MxM,NxC)
    #     row += [ks_CxC_CxM.statistic,ks_CxC_CxM.pvalue,ks_MxM_CxM.statistic,ks_MxM_CxM.pvalue]

    #     ks_CxC_CxN = stats.ks_2samp(CxC,NxC)
    #     ks_NxN_CxN = stats.ks_2samp(NxN,NxC)
    #     row += [ks_CxC_CxN.statistic,ks_CxC_CxN.pvalue,ks_NxN_CxN.statistic,ks_NxN_CxN.pvalue]

    #     ks_MxM_NxM = stats.ks_2samp(MxM,NxM)
    #     ks_NxN_NxM = stats.ks_2samp(NxN,NxM)
    #     row += [ks_MxM_NxM.statistic,ks_MxM_NxM.pvalue,ks_NxN_NxM.statistic,ks_NxN_NxM.pvalue]
        
    #     table.append(row)

    # columns = ['Go Term','Name','2007 Annos','2022 Annos','N','C','M','Mean NxN','Mean CxC','Mean MxM','Mean NxC','Mean NxM','Mean CxM','KS CxC CxM Statistic','KS CxC CxM P-Value','KS MxM CxM Statistic','KS MxM CxM P-Value','KS CxC CxN Statistic','KS CxC CxN P-Value','KS NxN CxN Statistic','KS NxN CxN P-Value','KS MxM NxM Statistic','KS MxM NxM P-Value','KS NxN NxM Statistic','KS NxN NxM P-Value']
    # pd.DataFrame(table,columns=columns).to_csv(f'Annotation_Correlation_Comparison_subset-{subsetSize}.csv',index=False)


    








if __name__ == '__main__':
    main()

