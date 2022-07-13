from cProfile import label
import torch
from PairwiseYeastData import PairwiseYeastData
from FlexNet import FlexNet
import torch.functional as F
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import time
from random import sample

class PairwiseModel():
    def __init__(self,data,fold,structure,folderName,modelName,lr=0.01,momentum=0.9,batch=20,activation='relu',inputDrop=None,hiddenDrop=None):
        #Pass in PairwiseYeastData
        self.data : PairwiseYeastData = data
        #Get training and validation data from specified fold of data
        self.posTrain, self.negTrain, self.posVal, self.negVal = data.getFold(fold)

        #Intializes network using number of input datasets and the specified hidden layer structure
        self.net = FlexNet(f'{len(self.data.datasets)}x{structure}',activation=activation,inputDrop=inputDrop,hiddenDrop=hiddenDrop)
        #Determines device the network will train on, then moves network to that device
        #self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.device = 'cpu'
        
        self.net.to(self.device)

        #Initializes loss function, Binary Cross Entropy loss
        self.lossFunc = nn.BCELoss()
        #Initializes optimizer variables and optimizer
        self.lr = lr
        self.momentum = momentum       
        self.opt = optim.SGD(self.net.parameters(),lr=self.lr,momentum=self.momentum)

        #Variable for the batch size of training inputs
        self.batch = batch
        self.fold = fold

        #Locations to save files
        self.dataTableLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}'
        self.networkLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}_Net_fold{fold+1}'
        self.lossLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}_Loss_fold{fold+1}.csv'

    def trainNetwork(self,epochs,printLoss=False,printTensors=False,regularize=True,lossFile='',saveLoss=True):
        start = time.time()
        #Make gene pairs from positive and negative training sets
        posPairs, negPairs = PairwiseYeastData.makePairs(self.posTrain,self.negTrain)
        running_loss = 0.0
        lossList = []
        #Loop over the number of epochs, which is really the number of batches
        for epoch in range(epochs):
            #Zeros out optimizer before each epoch
            self.opt.zero_grad()
            #Get list input batch array, which is an array of gene pairs
            inputArray = self.makeBatchArray(posPairs,negPairs)
            #Convert array of gene pairs into features and labels tensor for this batch of training
            features, labels = self.makeBatchTensors(inputArray,regularize=regularize)
            #Send features and labels to same device as network
            features = features.to(self.device)
            labels = labels.to(self.device)

            #Feed forward features tensor
            outputs = self.net(features.float())

            if(epoch %100 == 0 and epoch != 0 and printTensors):
                print(f'Input Array: {inputArray}')
                print(f'Features:')
                for i in range(len(features)):
                    print(features[i])
                print(f'Labels: {labels}')
                print(f'Outputs: {outputs}')

            #Calculate loss, the add loss to toal running loss
            
            loss = self.lossFunc(outputs.float(),labels.float())
            running_loss += loss.item()
            

            #Backpropagate, then update weights
            loss.backward()
            self.opt.step()
            

            #If printLoss is true, prints the running loss every 100 batches

            if(epoch % 100 == 0 and printLoss):
                print(f'Batch {epoch} Loss:\t{running_loss}',flush=True)
                lossList.append(running_loss)
                running_loss = 0.0
                print(f'Batch {epoch} Time:\t{(time.time()-start)/60} minutes',flush=True)
                start = time.time()
                if(saveLoss):
                    frame = pd.DataFrame(lossList,columns=['Loss'])
                    frame.to_csv(self.lossLocation,index=False)
        torch.save(self.net.state_dict(), f'{self.networkLocation}.pth')


    def testNetwork(self,save,testingType,limitNegative,negProportion=10,regularize=True,posProportion=0):
        with torch.no_grad():
            #Create positive and negative pairs from the validation data
            posPairs, negPairs = self.makeTestPairs(self.posVal,self.negVal)
            #Create an input array to make batch tensor by concatentating
            np.random.shuffle(posPairs)
            print(f'Pos pairs:')
            print(posPairs.shape)
            print('Neg Pairs')
            print(negPairs.shape)
            if posProportion == 0:
                posProportion = len(posPairs)
            if(limitNegative):
                np.random.shuffle(negPairs)
                inputArray = np.concatenate((posPairs[0:posProportion],negPairs[0:int(len(posPairs)*negProportion)]))
            else:
                inputArray = np.concatenate((posPairs[0:posProportion],negPairs))


            #Create features and labels tensors, then move them both to the gpu
            features, labels = self.makeBatchTensors(inputArray,regularize=regularize)
            features = features.to(self.device)
            labels = labels.to(self.device)

            #Feeds forward all of the validation data
            outputs = self.net(features.float(),test=True)

            #Turns input array of tuples into an array of gene pairs seperated by a space
            namesList = []
            foldsList = []
            gene1 = ''
            gene2 = ''
            for genePair in inputArray:
                namesList.append(f'{genePair[0]} {genePair[1]}')
                foldsList.append('NA')
                # for i in range(len(self.data.folds)):
                #     fold = self.data.folds[i]
                #     if(genePair[0] in fold[0] or genePair[0] in fold[1]):
                #         gene1 = f'{i+1}'
                #     if(genePair[1] in fold[0] or genePair[1] in fold[1]):
                #         gene2 = f'{i+1}'
                # foldsList.append(f'{gene1}_{gene2}')
            namesArray = np.array(namesList)
            foldsArray = np.array(foldsList)

            self.calcStats(namesArray=namesArray,labels=labels,foldsArray=foldsArray,outputs=outputs,save=save,testingType=testingType)

    #This method returns all the positive and negative pairs given an array of positive genes and an array of negative genes       
    def makeTestPairs(self,pos,neg):
        #This method is simple, but it is useful when we need to override it for the complex network
        return PairwiseYeastData.makePairs(pos,neg)
            

    def calcStats(self,namesArray,labels,foldsArray,outputs,save,testingType):
         #Moves labels and output tensors to cpu, then turns them into arrays and flattens them
        labelsArray = labels.cpu().numpy().flatten()
        outputsArray = outputs.cpu().numpy().flatten()

            #Concatenates arrays together, then transposes
        rawData = np.array([namesArray,labelsArray,foldsArray,outputsArray],dtype=object).transpose()
        #Sorts raw data by the fourth column, which is score in this case
        sortedData = rawData[rawData[:,3].argsort()]
            
        confusionMatrixList = []


        pos = 0
        neg = 0
        for row in sortedData:
            if(row[1] == 1):
                pos += 1
            else:
                neg += 1
        truePos = pos
        falsePos = neg
        trueNeg = 0
        falseNeg = 0
        for row in sortedData:
            if(row[1] == 1):
                truePos -= 1
                falseNeg += 1  
            else:
                falsePos -= 1
                trueNeg += 1
            confusionMatrixList.append(np.array([truePos,falsePos,trueNeg,falseNeg]))
        #Makes confusion matrix list into array
        confusionMatrix = np.array(confusionMatrixList)

        # truePos, trueNeg,falsePos, falseNeg = 0, 0, 0, 0
        # #In this loop, i represents the cutoff for what we consider a true postiive or negative
        # for i in range(len(sortedData)):
        #     #Loops over all genes determines where that gene is in the confusion matrix
        #     for j in range(len(sortedData)):
        #         #If gene is negative and below the line, it is a true negative
        #         if(sortedData[j,1] == 0.0 and j <= i):
        #             trueNeg += 1
        #         #If gene is positive and below the line, it is a false positive
        #         elif(sortedData[j,1] == 1.0 and j <= i):
        #             falseNeg += 1
        #         #If gene is negative and above the line, it is a false negative
        #         elif(sortedData[j,1] == 0.0 and j > i):
        #             falsePos += 1
        #         #If the gene is positive and above the line, it is a true positive
        #         else:
        #             truePos += 1
        #     #Appends an array of the confusion matrix value to a confusion matrix list
        #     confusionMatrixList.append(np.array([truePos,falsePos,trueNeg,falseNeg]))
        #     #Reset confusion matrix values
        #     truePos, trueNeg, falsePos, falseNeg = 0, 0 ,0 ,0

        
            
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

        dataTable = np.concatenate((sortedData,confusionMatrix,statisticsArray),1)  
        if(save):
                dataFrame = pd.DataFrame(dataTable,columns=['Name','+/-','Folds','Score','True Positive', 'False Positive', 'True Negative', 'False Negative', 'Accuracy', 'Precision', 'Recall', 'False Positive Rate', 'Selectivity'])
                dataFrame.to_csv(f'{self.dataTableLocation}_{testingType}_fold{self.fold+1}.csv') 
    


                



    def testNetworkTraining(self,save=True,regularize=True,limitNegative=False,negProportion=10,posProportion=0):
        self.testNetwork(save,'Train',regularize=regularize,limitNegative=limitNegative,negProportion=negProportion,posProportion=posProportion)
    
    def testNetworkValidation(self,save=True,regularize=True,limitNegative=False,negProportion=10,posProportion=0):
        self.testNetwork(save,'Val',regularize=regularize,limitNegative=limitNegative,negProportion=negProportion,posProportion=posProportion)


    def makeBatchArray(self,posPairs,negPairs):
        batchList =[]
        #Creates a list of random indicies for the positive and negative arrays
        posIndicies = np.random.choice(np.arange(len(posPairs)),int(self.batch/2),replace=False)
        negIndicies = np.random.choice(np.arange(len(negPairs)),int(self.batch/2),replace=False)
        #Adds the gene pair at each index to the batch list
        for index in posIndicies:
            batchList.append(posPairs[index])
        for index in negIndicies:
            batchList.append(negPairs[index])
        #Returns the batch as an array of gene pairs
        return np.array(batchList)

    def makeBatchTensors(self,inputArray,regularize=True):
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

            if(genePair[0] in self.data.posDataSet and genePair[1] in self.data.posDataSet):
                labelsList.append([1.0])
            else:
                labelsList.append([0.0])

        #Converts to tensor
        featuresTensor = torch.tensor(np.array(featuresList))
        labelsTensor = torch.tensor(labelsList)

        return (featuresTensor,labelsTensor)




