import torch
import numpy as np
import pandas as pd
from PairwiseModel import PairwiseModel
import torch.nn as nn
from PairwiseYeastData import PairwiseYeastData
from FlexNet import FlexNet
import torch.optim as optim

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves

from ExpressionDatasets import ExpressionDatasets


class ComplexModel(PairwiseModel):
    def __init__(self,fold,numFolds,structure,folderName,modelName,lr=0.01,momentum=0.9,batch=20):
        
        
        #Initialize a set of genes, then genes from all leaves
        self.genes = set()
        #Get genes for all terms with 10 or more genes
        leaves = getLeaves(10)
        #Loop that takes the union of all gene sets
        for leaf in leaves:
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

        self.net = FlexNet(f'{len(self.data.datasets)}x{structure}x{len(leaves)}',sigmoid=False)
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)

        self.lossFunc = nn.CrossEntropyLoss()
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)

        self.batch = batch



        
        
        

        self.loss = nn.CrossEntropyLoss()

