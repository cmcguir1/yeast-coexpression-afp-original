import torch
import numpy as np
import pandas as pd
from PairwiseModel import PairwiseModel
import torch.nn as nn
from PairwiseYeastData import PairwiseYeastData
from FlexNet import FlexNet
import torch.optim as optim
from random import sample

import sys
sys.path.append('./obopy/')
from Leaf import getLeaves

from ExpressionDatasets import ExpressionDatasets


class ComplexModel(PairwiseModel):
    def __init__(self,fold,numFolds,structure,folderName,modelName,lr=0.01,momentum=0.9,batch=20):
        
        
        #Initialize a set of genes, then genes from all leaves
        self.genes = set()
        #Get genes for all terms with 10 or more genes
        self.leaves = getLeaves(10)
        #Loop that takes the union of all gene sets
        for leaf in self.leaves:
            self.genes = self.genes | leaf[1]
        
        #Start and end index for fold slicing
        start = int((fold/numFolds)*len(self.genes))
        end = int(((fold+1)/numFolds)*len(self.genes))

        #Because there are no longer any positive or negative examples, we will store all genes in posTrain and posVal
        self.posVal = np.array(list(self.genes)[start:end])
        self.posTrain = np.array(list(self.genes - set(self.posVal)))
        #We still need negVal amd negTrain to exist, so we will make them empty arrays
        self.negVal = np.zeros((0,))
        self.negTrain = np.zeros((0,))

        #Make an array of all gene pairs
        pairs = PairwiseYeastData.makePairs(np.array(list(self.genes)),np.zeros((0,)))

        #For a complex model. the data field will be an instance of ExpressionDataset
        self.data = ExpressionDatasets(430,'./Yeast Resources/Datasets/All Spell/all spell datasets',pairs,200000,statsDictLoc='./Yeast Resources/Datasets/All Spell/statsDict.csv')

        self.net = FlexNet(f'{len(self.data.datasets)}x{structure}x{len(self.leaves)}',sigmoid=False)
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)

        self.lossFunc = nn.CrossEntropyLoss()
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)

        self.batch = batch

        self.dataTableLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}'
        self.networkLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}_Net_fold{fold+1}'
        self.lossLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}_Loss_fold{fold+1}.csv'

    #Overriden method for making batch arrays
    def makeBatchArray(self, posPairs, negPairs):
        #Take a random smaple from posPairs
        return np.array(sample(list(posPairs),self.batch))

    #Overriden method for making batch tensors
    def makeBatchTensors(self, inputArray, regularize=True):
        #Loop over all gene pairs in the input array
        featuresList = []
        labelsList = []
        for genePair in inputArray:
            correlations = []
            #Loops over all datasets
            for dataset in self.data.datasets:
                #Calculates the correlation coefficient between the expresssion levels of the two genes in a given data set, [0,1] is used because corrcoeff returns a matrix
                p = dataset.customCorrelation(genePair)
                #If p is 1 or -1, then there will be in error in arctanh, so make them 0.99 and -0.99
                if p == 1:
                    p = 0.99
                elif p == -1:
                    p = -0.99
                if(regularize):
                    correlations.append((np.arctanh(p) - dataset.mean)/dataset.std)
                else:
                    correlations.append(p)
   
            #Appends list of correlations to features list
            featuresList.append(correlations)
            
            label = []
            for leaf in self.leaves:
                if (genePair[0] in leaf[1] and genePair[1] in leaf[1]):
                    label.append(1.0)
                else:
                    label.append(0.0)
            labelsList.append(label)

        #Converts to tensor
        featuresTensor = torch.tensor(np.array(featuresList))
        labelsTensor = torch.tensor(labelsList)

        return (featuresTensor,labelsTensor)

