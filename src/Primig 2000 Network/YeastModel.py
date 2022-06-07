from cProfile import label
from random import random
from tokenize import String
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
        #self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.device = 'cpu'
        self.net.to(self.device)

        #Defines loss function, optimizer, and batch size
        self.lossFunc = nn.BCELoss()
        #We refactored the newtork to use nn.Sequential, so calling parameters() on the network works now
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)
        self.batch = batch_size

    #Training with replacement
    def trainNetwork(self,epochs):
        #Loop over the number of epochs, which in this case, is the number of batches
        running_loss = 0.0
        for epoch in range(epochs):
            #Create input and labels array
            inputArray, labelsArray = YeastModel.createNetworkArrays(self.posTrain,self.negTrain,self.batch)
            #Convert those arrays into tensors
            inputTensor, labelsTensor = YeastModel.createNetworkTensors(inputArray,labelsArray)
            #Move those tensor to same device as network
            inputTensor = inputTensor.to(self.device)
            labelsTensor = labelsTensor.to(self.device)

            #Zero gradients before making any calculations
            self.opt.zero_grad()
            #Feed forward
            outputs = self.net(inputTensor.float()) #This needs to be .float() for unknown reasons
            
            #Caculate loss, backpropagate, then update weights
            loss = self.lossFunc(outputs.float(),labelsTensor.float()) #I have no idea why this needs to be .long(), but it fixed the error
            running_loss += loss.item()
            loss.backward()
            self.opt.step()
            
            if(epoch % 100 == 0):
                print(f'Loss: {running_loss/100}')
                running_loss = 0.0



        

    #Creates input and output numpy array for 1 batch of network training
    def createNetworkArrays(positiveTraining,negativeTraining,batch_size):
        #Initializes arrays of ranges of indecies for positive and negative training arrays that will be used to index training tensors
        posList = np.arange(len(positiveTraining))
        negList = np.arange(len(negativeTraining))
        #Initializes input and output tensors of proper size filled with zeros
        inputs = np.zeros((batch_size,len(positiveTraining[0])-1)) #We subtract 1 from the len of posTrain[0] because the first colum, the name of the gene, is removed from the input array
        labels = np.empty((batch_size),dtype=object) #Right now we are going to make this a numpy array of strings
        #These two loops store the positive examples in the first half of the arrays, and the negative examples in the second half
        for i, index in enumerate(np.random.choice(posList,int(batch_size/2),replace=False),0):
            inputs[i] = positiveTraining[index,1:]
            labels[i] = positiveTraining[index,0]

        for i, index in enumerate(np.random.choice(negList,int(batch_size/2),replace=False)):
            inputs[i + int(batch_size/2)] = negativeTraining[index,1:]
            labels[i + int(batch_size/2)] = negativeTraining[index,0]
        #Returns inputs and labeels as a tuple
        return (inputs,labels)

    def createNetworkTensors(inputArray,labelsArray):
        #Converts numpy input array into numpy input tensor
        inputTensor = torch.from_numpy(inputArray)
        #Creates a tensor with all zeros that is the same length as the labels array

        labelsTensor = torch.zeros((len(labelsArray),1))

        #Loop over labels array, and if the the gene is a positive example, makes its associated index 1 for positive
        for gene in range(len(labelsArray)):
            if(labelsArray[gene] in YeastData.posSet):
                labelsTensor[gene][0] = 1.0
        #Return tuple of tensors, and converts them to float 64 tensors
        return (inputTensor.type(torch.float64),labelsTensor.type(torch.float64))
