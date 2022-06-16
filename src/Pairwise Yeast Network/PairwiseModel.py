import torch
from PairwiseYeastData import PairwiseYeastData
from FlexNet import FlexNet
import torch.functional as F
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd

class PairwiseModel():
    def __init__(self,data,fold,structure,folderName,modelName,lr=0.01,momentum=0.9,batch=20):
        #Pass in PairwiseYeastData
        self.data : PairwiseYeastData = data
        #Get training and validation data from specified fold of data
        self.posTrain, self.negTrain, self.posVal, self.negVal = data.getFold(fold)

        #Intializes network using number of input datasets and the specified hidden layer structure
        self.net = FlexNet(f'{len(self.data.datasets)}x{structure}')
        #Determines device the network will train on, then moves network to that device
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        # self.device = 'cpu'
        self.net.to(self.device)

        #Initializes loss function, Binary Cross Entropy loss
        self.lossFunc = nn.BCELoss()
        #Initializes optimizer variables and optimizer
        self.lr = lr
        self.momentum = momentum       
        self.opt = optim.SGD(self.net.parameters(),lr=self.lr,momentum=self.momentum)

        #Variable for the batch size of training inputs
        self.batch = batch

        #Locations to save files
        self.dataTableLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}_fold{fold+1}'
        self.networkLocation = f'./Yeast Networks/{folderName}/{modelName}_{structure}_fold{fold+1}'

    def trainNetwork(self,epochs,printLoss=False,printTensors=False,regularize=True):
        #Make gene pairs from positive and negative training sets
        posPairs, negPairs = PairwiseYeastData.makePairs(self.posTrain,self.negTrain)
        running_loss = 0.0
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

            if(epoch == 0 and printTensors):
                print(f'Input Array: {inputArray}')
                print(f'Features: {features}')
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
                print(f'Batch {epoch} Loss\t {running_loss}')
                running_loss = 0.0

    def testNetwork(self,save,testingType,regularize=True):
        with torch.no_grad():
            #Create positive and negative pairs from the validation data
            posPairs, negPairs = PairwiseYeastData.makePairs(self.posVal,self.negVal)
            #Create an input array to make batch tensor by concatentating 
            inputArray = np.concatenate((posPairs,negPairs))
            #Create features and labels tensors, then move them both to the gpu
            features, labels = self.makeBatchTensors(inputArray,regularize=regularize)
            features = features.to(self.device)
            labels = labels.to(self.device)

            #Feeds forward all of the validation data
            outputs = self.net(features.float())

            #Turns input array of tuples into an array of gene pairs seperated by a space
            namesList = []
            foldsList = []
            gene1 = ''
            gene2 = ''
            for genePair in inputArray:
                namesList.append(f'{genePair[0]} {genePair[1]}')
                for i in range(len(self.data.folds)):
                    fold = self.data.folds[i]
                    if(genePair[0] in fold[0] or genePair[0] in fold[1]):
                        gene1 = f'{i+1}'
                    if(genePair[1] in fold[0] or genePair[1] in fold[1]):
                        gene2 = f'{i+1}'
                foldsList.append(f'{gene1}_{gene2}')
            namesArray = np.array(namesList)
            foldsArray = np.array(foldsList)

            #Moves labels and output tensors to cpu, then turns them into arrays and flattens them
            labelsArray = labels.cpu().numpy().flatten()
            outputsArray = outputs.cpu().numpy().flatten()

            #Concatenates arrays together, then transposes
            rawData = np.array([namesArray,labelsArray,foldsArray,outputsArray],dtype=object).transpose()
            #Sorts raw data by the fourth column, which is score in this case
            sortedData = rawData[rawData[:,3].argsort()]
            
            confusionMatrixList = []

            truePos, trueNeg,falsePos, falseNeg = 0, 0, 0, 0
            #In this loop, i represents the cutoff for what we consider a true postiive or negative
            for i in range(len(sortedData)):
                #Loops over all genes determines where that gene is in the confusion matrix
                for j in range(len(sortedData)):
                    #If gene is negative and below the line, it is a true negative
                    if(sortedData[j,1] == 0.0 and j <= i):
                        trueNeg += 1
                    #If gene is positive and below the line, it is a false positive
                    elif(sortedData[j,1] == 1.0 and j <= i):
                        falseNeg += 1
                    #If gene is negative and above the line, it is a false negative
                    elif(sortedData[j,1] == 0.0 and j > i):
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

            dataTable = np.concatenate((sortedData,confusionMatrix,statisticsArray),1)
            if(save):
                dataFrame = pd.DataFrame(dataTable,columns=['Name','+/-','Folds','Score','True Positive', 'False Positive', 'True Negative', 'False Negative', 'Accuracy', 'Precision', 'Recall', 'False Positive Rate', 'Selectivity'])
                dataFrame.to_csv(f'{self.dataTableLocation}_{testingType}.csv')

                torch.save(self.net.state_dict(), f'{self.networkLocation}_{testingType}.pth')



    def testNetworkTraining(self,save=True,regularize=True):
        self.testNetwork(save,'Train',regularize=regularize)
    
    def testNetworkValidation(self,save=True,regularize=True):
        self.testNetwork(save,'Val',regularize=regularize)


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
                if(regularize):
                    correlations.append((np.arctanh(dataset.customCorrelation(genePair)) - dataset.mean)/dataset.std)
                else:
                    correlations.append(dataset.customCorrelation(genePair))


                # if(genePair[0] in dataset.geneDict and genePair[1] in dataset.geneDict and dataset.validGeneData(genePair)):
                #     #If regularize is true, z-score the fisher transform of the pearson correlation
                #     if(regularize):
                #         correlations.append((np.arctanh(np.corrcoef(dataset.geneDict[genePair[0]],dataset.geneDict[genePair[1]])[1,0]) - dataset.mean)/dataset.std)
                #     #Otherwise, just calculate the correlation between the data of the gene pair
                #     else:
                #         correlations.append(np.corrcoef(dataset.geneDict[genePair[0]],dataset.geneDict[genePair[1]])[1,0])
                # else:
                #     correlations.append(0.0)

                
            #Appends list of correlations to features list
            featuresList.append(correlations)

            if(genePair[0] in self.data.posDataSet and genePair[1] in self.data.posDataSet):
                labelsList.append([1.0])
            else:
                labelsList.append([0.0])

        #Converts to tensor
        featuresTensor = torch.tensor(np.array(featuresList))
        labelsTensor = torch.tensor(labelsList)

        #Creates labels tensor, which shoudl always have the first hald of the values be [1] and the second half be [0]
        # labelsList = []
        # for genePair in
        # for i in range(int(self.batch/2)):
        #     labelsList.append([1.0])
        # for i in range(int(self.batch/2)):
        #     labelsList.append([0.0])
        # labelsTensor = torch.tensor(labelsList)
        #Returns tuple of tensors
        return (featuresTensor,labelsTensor)




