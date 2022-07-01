import torch
import numpy as np
import pandas as pd
from PairwiseModel import PairwiseModel
import torch.nn as nn
from PairwiseYeastData import PairwiseYeastData
from FlexNet import FlexNet
import torch.optim as optim
from random import sample, shuffle

import sys
sys.path.append('./obopy/')
from Leaf import getLeaves

from ExpressionDatasets import ExpressionDatasets


class ComplexModel(PairwiseModel):
    def __init__(self,fold,numFolds,structure,folderName,modelName,lr=0.01,momentum=0.9,batch=20,foldFile='',numTerms=0):
        #Initialize a set of genes, then genes from all leaves
        self.genes = set()
        #Get genes for all terms with 10 or more genes
        if numTerms == 0:
            self.leaves = getLeaves(10)
        else:
            self.leaves = getLeaves(10)[0:numTerms]
        #Loop that takes the union of all gene sets
        for leaf in self.leaves:
            self.genes = self.genes | leaf[1]
        #This instance variable will be useful making new gene folds
        self.numFolds = numFolds


        if foldFile == '':
            #Start and end index for fold slicing
            start = int((fold/numFolds)*len(self.genes))
            end = int(((fold+1)/numFolds)*len(self.genes))

            #Because there are no longer any positive or negative examples, we will store all genes in posTrain and posVal
            self.posVal = np.array(list(self.genes)[start:end])
            self.posTrain = np.array(list(self.genes - set(self.posVal)))
            #We still need negVal amd negTrain to exist, so we will make them empty arrays
        else:
            val = []
            train = []
            geneFolds = pd.read_csv(foldFile).to_numpy()
            for gene in geneFolds:
                if gene[1] == fold:
                    val.append(gene[0])
                else:
                    train.append(gene[0])
            self.posVal = np.array(val)
            self.posTrain = np.array(train)

        self.negVal = np.zeros((0,))
        self.negTrain = np.zeros((0,))

        #Make an array of all gene pairs
        pairs = PairwiseYeastData.makePairs(np.array(list(self.genes)),np.zeros((0,)))

        #For a complex model. the data field will be an instance of ExpressionDataset
        self.data = ExpressionDatasets(430,'./Yeast Resources/Datasets/All Spell/all spell datasets',pairs,200000,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv')

        self.net = FlexNet(f'{len(self.data.datasets)}x{structure}x{len(self.leaves)}',sigmoid=False)
        self.device = 'cpu'
        #self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)

        self.lossFunc = nn.CrossEntropyLoss()
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)

        self.batch = batch
        self.fold = fold

        self.dataTableLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}'
        self.networkLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}_Net_fold{fold+1}'
        self.lossLocation = f'./Yeast Resources/Pairwise/{folderName}/{modelName}_{structure}_Loss_fold{fold+1}.csv'

    #Overriden method for making batch arrays
    def makeBatchArray(self, posPairs, negPairs):
        #Take a random smaple from posPairs
        return np.array(sample(list(posPairs),self.batch))

    def makeFolds(self,location):
        genesList = list(self.genes)
        shuffle(genesList)
        foldTable = []
        for fold in range(self.numFolds):
            for i in range(int((fold/self.numFolds)*len(self.genes)),int(((fold+1)/self.numFolds)*len(self.genes))):
                foldTable.append([genesList[i],fold])
        pd.DataFrame(foldTable,columns=['Gene','Fold']).to_csv(location,index=False)


        

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

    def calcStats(self,namesArray, labels, foldsArray, outputs,save,testingType):
        labelsArray = labels.cpu().numpy().transpose()
        outputsArray  = outputs.cpu().numpy().transpose()
        goData = [namesArray,foldsArray]
        colNames = ['Name','Fold']
        goStats = []
        for i in range(len(labelsArray)):
            print(f'Calculating term: {i}')
            goData.append(labelsArray[i])
            goData.append(outputsArray[i])
            colNames.append(f'Labels {self.leaves[i][0]}')
            colNames.append(f'Score {self.leaves[i][0]}')
            goStats.append(ComplexModel.calcGOStats(namesArray,goData[-2],goData[-1],self.leaves[i][0]))
            
        goData = np.array(goData).transpose()
        goStats = np.array(goStats)
        print(goData)
        print(goStats)
        dataFrame = pd.DataFrame(goData,columns=colNames)
        statsFrame = pd.DataFrame(goStats,columns=['GO Term','AUC','Average Precision'])
        dataFrame.to_csv(f'{self.dataTableLocation}_{testingType}_data_fold{self.fold+1}.csv',index=False)
        statsFrame.to_csv(f'{self.dataTableLocation}_{testingType}_stats_fold{self.fold+1}.csv',index=False)
        
        

    def calcGOStats(names,labels,outputs,term):
        rawData = np.array([names,labels,outputs],dtype=object).transpose()
        #Sorts raw data by the fourth column, which is score in this case
        sortedData = rawData[rawData[:,2].argsort()]
            
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
        # #Makes confusion matrix list into array
        # confusionMatrix = np.array(confusionMatrixList)
            
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

        precisionArray = np.copy(statisticsArray[:,1])
        for i in range(len(precisionArray)-1,0,-1):
            if (precisionArray[i-1] < precisionArray[i]):
                precisionArray[i-1] = precisionArray[i]

        averagePre = np.mean(precisionArray)
        auc = np.mean(statisticsArray[:,2])
        return([term,auc,averagePre])


        


        
            
        

