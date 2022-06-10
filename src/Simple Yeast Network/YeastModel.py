from cProfile import label
from random import random
import statistics
from tokenize import String
from aiohttp import TraceRequestExceptionParams
from sklearn.metrics import precision_recall_curve
import torch
from YeastData import YeastData
from PrimigNets import PrimegNet
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd


class YeastModel():
    def __init__(self,fold,yeastData,structure,lr,momentum,batch_size,dataName):
        #Initialize a yeast data set from passed in reference
        self.data = yeastData
        #Retrieve training and validation data from dataset, all of these variables are tensors
        self.posTrain, self.negTrain, self.posVal, self.negVal = self.data.getFold(fold)
        
        #Initialize network of a specified structure, then moves network to gpu if available
        self.net = PrimegNet(structure)
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)

        #Defines loss function, optimizer, and batch size
        self.lossFunc = nn.BCELoss()
        #We refactored the newtork to use nn.Sequential, so calling parameters() on the network works now
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)
        self.batch = batch_size

        #File path where data table and network should be saved

        folderName = 'June-9-Reruns'
        self.dataFilePath = f'./Yeast Resources/{folderName}/{dataName}_{structure}_fold{fold+1}'
        self.networkFilePath = f'./Yeast Networks/{folderName}/{dataName}_{structure}_fold{fold+1}'
        self.valFold = f'./Yeast Resources/{folderName}/{dataName}_{structure}_fold{fold+1}_ValGenes'

    #Training with replacement
    def trainNetwork(self,epochs,collectData=False,filePath=''):
        #Loop over the number of epochs, which in this case, is the number of batches
        running_loss = 0.0
        runningLossList = []
        for epoch in range(epochs):
            #Create input and labels array
            inputArray, labelsArray = YeastModel.createTrainArrays(self.posTrain,self.negTrain,self.batch)
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
                runningLossList.append(np.array([epoch,running_loss]))
                running_loss = 0.0
        if(collectData):
            runningLossArray = np.array(runningLossList)
            lossData = pd.DataFrame(runningLossArray,columns=['Batches','Loss'])
            lossData.to_csv(filePath)

    def testNetwork(self,inputs,labels,testingType,save):
        #Takes inputs and labels arrays and converts them to tensors, then moves those tensors to device
        inputTensor, labelsTensor = YeastModel.createNetworkTensors(inputs,labels)
        inputTensor = inputTensor.to(self.device)
        labelsTensor = labelsTensor.to(self.device)
        
        with torch.no_grad():
            #Forward feeds inputs through network
            outputs = self.net(inputTensor.float())
            #Flattens output tensor, then converts it into a numpy array
            outputs = torch.flatten(outputs)
            outputsArray = outputs.cpu().numpy()
            #Flattens labels tensor, then convert Labels tensor into array to be used in data table
            labelsTensor = torch.flatten(labelsTensor)
            labelsArray = labelsTensor.cpu().numpy()

            #Creates array of gene name, labels, and output value arrays, then flips rows and columns of array
            rawData = np.array((labels,labelsArray,outputsArray),dtype=object)
            rawDataList = []
            for i in range(len(outputsArray)):
                rawDataList.append(rawData[:,i])
            rawData = np.array(rawDataList,dtype=object)
            #Sorts rawData array by the output value of each row
            sortedRawData = rawData[rawData[:,2].argsort()]

            confusionMatrixList = []
            truePos = 0
            falsePos = 0
            trueNeg = 0
            falseNeg = 0
            #In this loop, i represents the cutoff for what we consider a true postiive or negative
            for i in range(len(sortedRawData)):
                #Loops over all genes determines where that gene is in the confusion matrix
                for j in range(len(sortedRawData)):
                    #If gene is negative and below the line, it is a true negative
                    if(sortedRawData[j,1] == 0.0 and j <= i):
                        trueNeg += 1
                    #If gene is positive and below the line, it is a false positive
                    elif(sortedRawData[j,1] == 1.0 and j <= i):
                        falseNeg += 1
                    #If gene is negative and above the line, it is a false negative
                    elif(sortedRawData[j,1] == 0.0 and j > i):
                        falsePos += 1
                    #If the gene is positive and above the line, it is a true positive
                    else:
                        truePos += 1
                #Appends an array of the confusion matrix value to a confusion matrix list
                confusionMatrixList.append(np.array([truePos,falsePos,trueNeg,falseNeg]))
                #Reset confusion matrix values
                truePos, trueNeg, falsePos, falseNeg = 0, 0 ,0 ,0
            #Makes confusion matrix list into array
            confusionMatrix = np.array(confusionMatrixList)
            
            #Calculate statistics for confusion matrix array
            statisticsList = []
            for mat in confusionMatrix:
                accuracy = (mat[0] + mat[2]) / mat.sum()
                precision = 1 if (mat[0] + mat[1] == 0) else (mat[0]) / (mat[0] + mat[1])
                recall =  1 if(mat[0] + mat[3] == 0) else mat[0] / (mat[0] + mat[3])
                falsePositiveRate = mat[1] / (mat[1] + mat[2])
                selectivity = mat[2] /(mat[2] + mat[1])
                statisticsList.append(np.array([accuracy,precision,recall,falsePositiveRate,selectivity]))
            #Converts stats list into array to be concatenated
            statisticsArray = np.array(statisticsList)

            #Concatenate data arrays together to form final data table
            dataTable = np.concatenate((sortedRawData,confusionMatrix,statisticsArray),1)
            
            #Create DataFrame from array, then save it to dataFilePath if save is True
            if(save):
                dataFrame = pd.DataFrame(dataTable,columns=['Name','+/-','Score','True Positive', 'False Positive', 'True Negative', 'False Negative', 'Accuracy', 'Precision', 'Recall', 'False Positive Rate', 'Selectivity'])
                dataFrame.to_csv(f'{self.dataFilePath}_{testingType}.csv')

                #Save network to networkFilePath
                torch.save(self.net.state_dict(), f'{self.networkFilePath}_{testingType}.pth')

                #Save list of gene in positive set and list in negative set
                #self.saveFoldGeneVal()

    def saveFoldGeneVal(self):
        posFrame = pd.DataFrame(self.posVal[:,0],columns=["NAME"])
        posFrame.to_csv(f'{self.valFold}_Pos.csv',index=False)
        negFrame = pd.DataFrame(self.negVal[:,0],columns=['NAME'])
        negFrame.to_csv(f'{self.valFold}_Neg.csv',index=False)

    #Three methods that pass that help pass the right data arrays to testNetwork
    def testNetworkTrain(self,save=True):
        inputs, labels = YeastModel.createTestArrayDouble(self.posTrain,self.negTrain)
        self.testNetwork(inputs,labels,'Train',save)

    def testNetworkVal(self,save=True):
        inputs, labels = YeastModel.createTestArrayDouble(self.posVal,self.negVal)
        self.testNetwork(inputs,labels,'Val',save)

    def testNetworkTest(self,save=True):
        inputs, labels = YeastModel.createTestArraySingle(self.data.testingData)
        self.testNetwork(inputs,labels,'Test',save)

    #Creates input and output numpy array for 1 batch of network training
    def createTrainArrays(positiveTraining,negativeTraining,batch_size):
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

    #Version of function that combines the positive and negative data into an input and labels array
    def createTestArrayDouble(positiveTest,negativeTest):
        inputsList = []
        labelsList = []
        for i in range(len(positiveTest)):
            inputsList.append(positiveTest[i,1:])
            labelsList.append(positiveTest[i,0])
        for i in range(len(negativeTest)):
            inputsList.append(negativeTest[i,1:])
            labelsList.append(negativeTest[i,0])
        inputArray = np.array(inputsList)
        labelsArray = np.array(labelsList)
        return (inputArray,labelsArray)

    #Version of function converts a single input array into an input and labels array
    def createTestArraySingle(testData):
        inputList = []
        labelsList = []
        for i in range(len(testData)):
            inputList.append(testData[i,1:])
            labelsList.append(testData[i,0])
        #Because inputList is a list of arrays, calling np.array creates a
        inputArray = np.array(inputList)
        labelsArray = np.array(labelsList)
        return (inputArray,labelsArray)
        

    def createNetworkTensors(inputArray,labelsArray):
        #Converts numpy input array into numpy input tensor, must convert input array into float64 array
        inputTensor = torch.from_numpy(inputArray.astype('float64'))
        #Creates a tensor with all zeros that is the same length as the labels array

        labelsTensor = torch.zeros((len(labelsArray),1))

        #Loop over labels array, and if the the gene is a positive example, makes its associated index 1 for positive
        for gene in range(len(labelsArray)):
            if(labelsArray[gene] in YeastData.posSet):
                labelsTensor[gene][0] = 1.0
        #Return tuple of tensors, and converts them to float 64 tensors
        return (inputTensor.type(torch.float64),labelsTensor.type(torch.float64))
