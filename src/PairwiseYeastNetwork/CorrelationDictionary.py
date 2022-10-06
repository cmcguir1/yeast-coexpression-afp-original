from textwrap import indent
import numpy as np
import pandas as pd
from ExpressionDatasets import ExpressionDatasets

class CorrelationDictionary():
    def __init__(self,dictLoc='../YeastCorrDictionary.dat'):
        #Dictionary of Gene Name to its index in the correlation dictionary
        self.genes = pd.read_csv('./src/PairwiseYeastNetwork/geneIndexDictionary_full.csv').to_numpy()
        self.indexDict = {gene[0]: gene[1] for gene in self.genes}
        # print(f'Index Dict: {self.indexDict}\n----------------------------')

        self.geneNumber = len(self.genes)

        self.pairs = np.array([[self.genes[i,0],self.genes[j,0]] for i in range(len(self.genes)) for j in range(i,len(self.genes))])

        #Dictionary of dataset same to index of dataset in gene dictionary
        datasets = pd.read_csv('./src/PairwiseYeastNetwork/datasetDictionary.csv').to_numpy()
        self.datasetsDict = {data[0]: data[1] for data in datasets}
        self.datasets = datasets[:,0]

        #Expression Datasets that will be used to calculate the pair correlations that wil be saved to the memory mapped numpy arrays
        self.expDataset = ExpressionDatasets('./Yeast Resources/Datasets/All Spell/all spell datasets',sort=True,recur=True,recalc=False,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv')
        
        #Correlations dictionary initialization
        self.memMap = np.memmap(dictLoc,mode='w+',shape=(len(self.datasets),(self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber))

    def lookupCorrelation(self,gene1,gene2,dataset):
        #print(f'Gene 1: {gene1}\nGene: {gene2}\n------------')
        if gene1 in self.indexDict and gene2 in self.indexDict:
            return self.memMap[self.datasetsDict[dataset],self.calcIndex(gene1,gene2)]
        else:
            return 0
    
    
    def calculateDataset(self,datasetIndex,location='./MemoryMapTest.dat'):
        memMap = np.memmap(location,dtype='float32',mode='w+',shape=((self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber,))
        for pair in self.pairs:
            # print(pair)
            dset = self.expDataset.datasets[datasetIndex]
            val = dset.customCorrelation(pair)
            memMap[self.calcIndex(pair[0],pair[1])] = val
        memMap.flush()

    def calcIndex(self,gene1,gene2):
        if self.indexDict[gene1] > self.indexDict[gene2]:
            row = self.indexDict[gene1]
            col = self.indexDict[gene2]
        else:
            col = self.indexDict[gene1]
            row = self.indexDict[gene2]
        return (col * self.geneNumber - sum(range(col))) + row

    def unifyCorrelations(self,absLocation):
        memMap = np.memmap(absLocation,'float32',mode='w+',shape =(len(self.datasets),(self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber))
        for dataset, index in self.datasetsDict:
            memMap[self.expDataset[dataset]] = np.memmap(f'/home/cmcguir1/YeastMemMap/{dataset}_corrDict.dat',mode='w+',shape=((self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber,))
            memMap.flush()
