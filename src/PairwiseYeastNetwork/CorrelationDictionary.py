from operator import index
from textwrap import indent
import numpy as np
import pandas as pd
from pyparsing import col
from sympy import pdsolve
from ExpressionDatasets import ExpressionDatasets
import time
import sys

class CorrelationDictionary():
    def __init__(self,dictLoc='../YeastDict_float16.npy',datasetType='modern'):
        #Dictionary of Gene Name to its index in the correlation dictionary
        self.genes = pd.read_csv('./src/PairwiseYeastNetwork/geneIndexDictionary_full.csv').to_numpy()
        self.indexDict = {gene[0]: gene[1] for gene in self.genes}
        # print(f'Index Dict: {self.indexDict}\n----------------------------')

        self.geneNumber = len(self.genes)
        

        #Dictionary of dataset same to index of dataset in gene dictionary
        datasets = pd.read_csv('./src/PairwiseYeastNetwork/datasetDictionaryRevised.csv' if datasetType != '2009' and datasetType != 'original' else './src/PairwiseYeastNetwork/datasetDictionaryOriginal.csv').to_numpy()
        self.datasetsDict = {data[0]: data[1] for data in datasets}
        self.datasets = datasets[:,0]


        #Expression Datasets that will be used to calculate the pair correlations that wil be saved to the memory mapped numpy arrays
        if datasetType == '2009' or datasetType == 'original':
            print('Used 2009 Datasets')
            self.expDataset = ExpressionDatasets('./Yeast Resources/Datasets/All Spell/original',sort=False,recur=False,recalc=False)
        else:
            self.expDataset = ExpressionDatasets('./Yeast Resources/Datasets/All Spell/all spell datasets',sort=True,recur=True,recalc=False,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv')
            print('Used Modern Datasets')

        
        # Correlations dictionary initialization
        # self.memMap = np.memmap(dictLoc,'float32',mode='r+',shape=(430,(self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber))
        self.memMap = np.load(dictLoc)
        print(f'Correlation Dictionary: {sys.getsizeof(self.memMap)}')
        print(f'Expression Datasets: {sys.getsizeof(self.expDataset)}')


    def lookupCorrelation(self,gene1,gene2,dataset):
        #print(f'Gene 1: {gene1}\nGene: {gene2}\n------------')
        if gene1 in self.indexDict and gene2 in self.indexDict:
            return self.memMap[self.datasetsDict[dataset],self.calcIndex(gene1,gene2)]
        else:
            #print('This gene pair was not in the correlation dictionary')
            return 0
    
    
    def calculateDataset(self,datasetIndex,location='./RecalcTest.npy'):
        # memMap = np.memmap(location,dtype='float32',mode='r+',shape=((self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber,))
        self.pairs = np.array([[self.genes[i,0],self.genes[j,0]] for i in range(len(self.genes)) for j in range(i,len(self.genes))])
        memMap = np.zeros(shape=((self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber,),dtype=np.float16)
        start = time.time()
        for i, pair in enumerate(self.pairs):
            dset = self.expDataset.datasets[datasetIndex]
            val = dset.customCorrelation(pair,regularize=True)
            memMap[self.calcIndex(pair[0],pair[1])] = val
            if i % 100000 == 0:
                print(f'Time for 100000 pairs: {(time.time()-start)/60}')
                start = time.time()
        np.save(location,memMap)

    def calcIndex(self,gene1,gene2):
        if self.indexDict[gene1] > self.indexDict[gene2]:
            row = self.indexDict[gene1]
            col = self.indexDict[gene2]
        else:
            col = self.indexDict[gene1]
            row = self.indexDict[gene2]
        return (col * self.geneNumber - sum(range(col))) + row

    def unifyCorrelations(self,absLocation):
        memMap = np.zeros((len(self.datasets),(self.geneNumber*self.geneNumber - sum(range(self.geneNumber))+self.geneNumber)),dtype=np.float16)
        # memMap = np.memmap(absLocation,'float32',mode='w+',shape =(len(self.datasets),(self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber))
        
        for dataset in self.datasets:
            # memMap[self.datasetsDict[dataset],:] = np.memmap(f'/home/cmcguir1/data/YeastMemMap/{dataset}_corrDict.dat',mode='r+',shape=((self.geneNumber*self.geneNumber - sum(range(self.geneNumber))) + self.geneNumber,))
            memMap[self.datasetsDict[dataset],:] = np.load(f'../YeastMemMap_ReCalc/{dataset}_correlations.npy')
        np.save(absLocation,memMap)
