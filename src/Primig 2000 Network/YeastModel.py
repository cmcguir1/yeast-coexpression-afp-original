from random import random
import torch
from YeastData import YeastData
from PrimigNets import PrimegNet
import torch.nn as nn
import torch.optim as optim
import numpy as np


class YeastModel():
    def __init__(self,fold,percentTest,numFolds,structure,lr,momentum,batch_size):
        #Initialize a yeast dataset, then retrieve partions
        self.data = YeastData(percentTest,numFolds)
        #Retrieve training and validation data from dataset, all of these variables are tensors
        self.posTrain, self.negTrain, self.posVal, self.negVal = self.data.getFold(fold)
        
        #Initialize network of a specified structure, then moves network to gpu if available
        self.net = PrimegNet(structure)
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)

        #Defines loss function, optimizer, and batch size
        self.lossFunc = nn.CrossEntropyLoss()
        #We refactored the newtork to use nn.Sequential, so calling parameters() on the network works now
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)
        self.batch = batch_size

    #Training with replacement
    def trainNetwork(self,epochs):
        #Initializes arrays of ranges of indecies for positive and negative training arrays that will be used to index training tensors
        posList = np.arange(len(self.posTrain))
        negList = np.arange(len(self.negTrain))
        #Initializes input and output tensors of proper size filled with zeros
        inputs = np.zeros((self.batch,len(self.posTrain[0])-1)) #We subtract 1 from the len of posTrain[0] because the first colum, the name of the gene, is removed from the input array
        outputs = np.zeros((self.batch))
        #In this case, each epoch is a single batch
        for epoch in range(epochs):
            for i, index in enumerate(np.random.choice(posList,int(self.batch/2),replace=False),0):
                inputs[i] = self.posTrain[index,1:]
                outputs[i] = self.posTrain[index,0]

            for i, index in enumerate(np.random.choice(negList,int(self.batch/2),replace=False)):
                inputs[i + (self.batch/2)] = self.negTrain[index,1:]
                outputs[i] = self.negTrain[index,0]