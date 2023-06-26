from typing import Any
import pandas as pd
import torch
from torch.utils.data import Dataset
from CorrelationDictionary import CorrelationDictionary
import os

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes


class CustomDataset(Dataset):
    def __init__(self,ontologyDataset,inputVector,outputVector,memMapName):
        self.inputSize = 0

        # These four booleans are used for control flow later of data inclusion throughout the Model Object
        self.expression = 'x' in inputVector
        self.localization = 'l' in inputVector
        self.genomicInteraction = 'g' in inputVector
        self.physical = 'p' in inputVector

        if self.expression:
            # Correlations Dictionary that will be retrieve precalculated correlation values
            # self.corrDict = CorrelationDictionary(dictLoc='../YeastMemMap/YeastDict_float16.npy' if (os.path.exists('../YeastMemMap/YeastDict_float16.npy')) else '../YeastDict_float16.npy',datasetType=ontologyDataset)
            self.corrDict = CorrelationDictionary(dictLoc=f'../YeastMemMap/{memMapName}' if (os.path.exists(f'../YeastMemMap/{memMapName}')) else f'../{memMapName}',datasetType=ontologyDataset)
            
            self.datasets = self.corrDict.expDataset.datasets
            self.inputSize += len(self.datasets)
            print('Initialized Expression Datasets')

        if self.localization:
            # Localization Data Map
            localizationData = pd.read_csv('./Yeast Resources/Datasets/All Spell/YeastLocalizationData.txt',sep="\t",index_col=False).drop(['Unnamed: 32'],axis=1).to_numpy()
            self.localMap = {}
            for row in localizationData:
                self.localMap[row[1]] = [local == 'T' for local in row[9:]]
            self.inputSize += 23
            print('Initialized Localization Data')

        if self.genomicInteraction:
            # Dataset of all bioGRID interactions
            interactions = pd.read_csv('./InteractionData.txt',sep="\t").to_numpy()
            interactionsList = pd.read_csv('./bioGRID_Interactions.csv').to_numpy().flatten()
            # genomic index maps the genomic interactions we care about to an index
            genomicIndex = {item: i for i, item in enumerate(interactionsList[9:])}
            
            self.genomicMap = {}
            for row in interactions:
                # The string of the concatenated gene pair must be stored for both orders of which gene is first
                genePairStrA = row[0] + " " + row[1]
                genePairStrB = row[1] + " " + row[0]
                if (not (genePairStrA in self.genomicMap)) or (not (genePairStrB in self.genomicMap)):
                    self.genomicMap[genePairStrA] = [0 for i in range(6)]
                    self.genomicMap[genePairStrB] = [0 for i in range(6)]
                if row[6] in genomicIndex:
                    # If a gene pair has a interaction, change the value of the interactions list for that pair from 0 to 1 at that specific interaction's index
                    tmp = self.genomicMap[genePairStrA]
                    tmp[genomicIndex[row[6]]] = 1
                    self.genomicMap[genePairStrA] = tmp
                    self.genomicMap[genePairStrB] = tmp
            
            self.inputSize += 6
                

        if self.physical:
            # Dataset of all bioGRID interactions
            interactions = pd.read_csv('./InteractionData.txt',sep="\t").to_numpy()
            interactionsList = pd.read_csv('./bioGRID_Interactions.csv').to_numpy().flatten()
            
            # physical index maps physical interactions to indicies
            physicalIndex = {item: i for i, item in enumerate(interactionsList[2:9])}
            # All types of affinity capture are represented by one node, so they are all mapped to index 0
            physicalIndex['Affinity Capture-MS'] = 0
            physicalIndex['Affinity Capture-Western'] = 0
            
            
            self.physicalMap = {}
            for row in interactions:
                # The string of the concatenated gene pair must be stored for both orders of which gene is first
                genePairStrA = row[0] + " " + row[1]
                genePairStrB = row[1] + " " + row[0]
                if (not (genePairStrA in self.physicalMap)) or (not (genePairStrB in self.physicalMap)):
                    self.physicalMap[genePairStrA] = [0 for i in range(7)]
                    self.physicalMap[genePairStrB] = [0 for i in range(7)]
                if row[6] in physicalIndex:
                    # If a gene pair has a interaction, change the value of the interactions list for that pair from 0 to 1 at that specific interaction's index
                    tmp = self.physicalMap[genePairStrA]
                    tmp[physicalIndex[row[6]]] = 1
                    self.physicalMap[genePairStrA] = tmp
                    self.physicalMap[genePairStrB] = tmp
            
            self.inputSize += 7


        #   outputVector determines what types of GO terms are included as labels for the output vector
        #       b - Biological Processes
        #       m - Molecular Functions
        #       c - Cellular Components   
        #       n - non specific gene pair interaction (co-annotated to any biological process)    
        #   Additional GO terms can be added with 'addTerm'
        
        self.leaves = getLeaves(10,dataset=ontologyDataset,bioProc=('b' in outputVector),molFunc=('m' in outputVector),cellComp=('c' in outputVector))
        for term in addTerms:
            self.leaves.append([term,set(getGenes(term,dataset=ontologyDataset))])
        self.GOTermDict = {term[0]: i for i,term in enumerate(self.leaves)}
        self.outputSize = len(self.leaves)
        
        self.nonSpecific = 'n' in outputVector
        if self.nonSpecific:
            self.outputSize += 1
        

    def __len__(self):
        pass
    
    def __getitem__(self):
        pass

    