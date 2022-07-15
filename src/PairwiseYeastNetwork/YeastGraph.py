import torch
import numpy as np
import pandas as pd
from FlexNet import FlexNet
from PairwiseModel import PairwiseModel
from PairwiseYeastData import PairwiseYeastData
import time


class YeastGraph(PairwiseModel):
    def __init__(self,networkPath,data,structure,posFile,negFile,agnFile,includeAll=True):
        #Intialize PairwiseYeastData as data
        self.data : PairwiseYeastData = data

        #Initialize an untrained network, then load in a trained network from memory
        self.net = FlexNet(structure=structure)
        self.net.load_state_dict(torch.load(networkPath))
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)

        #Intialize pos, neg, and agn gene arrays, then concatentate them together
        posGenes = pd.read_csv(posFile).to_numpy().flatten()
        negGenes = pd.read_csv(negFile).to_numpy().flatten()
        agnGenes = pd.read_csv(agnFile).to_numpy().flatten()
        self.genes = np.concatenate([posGenes,negGenes,agnGenes],0)
        #If includeAll is true, make every gene pair
        if(includeAll):
            self.pairs = self.makePairs(self.genes)
        #Otherwise, only make gene pairs that include at least 1 positive
        else:
            self.pairs = self.makePosPairs(posGenes,self.genes)

        #Create a positive gene set from positive gene array
        self.posSet = set(posGenes)
        self.agnSet= set(agnGenes)
        self.negSet = set(negGenes)

        #Make the batch size equal to the number of gene pairs
        self.batch = len(self.pairs)

    #Passes all gene pairs through network, then saves a data table of their outputs
    def feedForward(self,fileLocation,save=True):
        # features, labels = self.makeBatchTensors(self.pairs)
        # features = features.to(self.device)
        # with torch.no_grad():
        #     outputs = self.net(features.float(),test=True)

        #Revised feed forward algoritm that passes one gene into the network at a time
        outputsList = []
        with torch.no_grad():
            #Loop over all genes in the array of pairs, pass in a gene to the network, then append its output to the output list
            for i, pair in enumerate(self.pairs,0):
                start = time.time()
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                outputsList.append(self.net(features.float(),test=True).cpu().flatten()[0])
                if(i % 100 == 0):
                    print(f'Pairs Calculated: {i+1}/{len(self.pairs)}',flush=True)
                    print(f'Time to calculate: {(time.time()-start)/60} minutes',flush=True)
        outputs = np.array(outputsList)


        self.dataTable = np.array([self.pairs[:,0],self.pairs[:,1],outputs],dtype=object).transpose()
        if(save):
            dataFrame = pd.DataFrame(self.dataTable,columns=['Gene A', 'Gene B', 'Score'])
            dataFrame.to_csv(fileLocation,index=False)

    #Ranks genes by the strength of their connections to positive genes
    def rankGenes(self,filePath,dataTablePath=''):

        if(not(dataTablePath=='')):
            self.dataTable = pd.read_csv(dataTablePath).to_numpy()
        #Intializes empty dictionary, then makes all genes keys to the number 0
        scoreDict = {}
        for gene in self.genes:
            scoreDict[gene] = 0
        #Loops over all genes in the data Table
        for genePair in self.dataTable:
            #If gene A is positive, then add the score of the pair to Gene B
            if(genePair[0] in self.posSet):
                scoreDict[genePair[1]] = scoreDict[genePair[1]] + genePair[2]
            #If gene B is positive, add the score to gene A
            if(genePair[1] in self.posSet):
                scoreDict[genePair[0]] = scoreDict[genePair[0]] + genePair[2]
        #Turn of genes and score into list
        dataTable = []
        for gene in self.genes:
            #This conditional determines what the sign of each gene is
            if(gene in self.posSet):
                sign = 1
            elif(gene in self.agnSet):
                sign = 0
            else:
                sign = -1
            dataTable.append([gene,sign,scoreDict[gene]])

        #Convert list to array, then sort it by score in reverse order
        dataArray = np.array(dataTable,dtype=object)
        sortedData = dataArray[dataArray[:,2].argsort()[::-1]]

        confusionMatrixList = []
        pos = 0
        neg = 0
        for row in sortedData:
            if(row[1] == 1):
                pos += 1
            else:
                neg += 1
        truePos = 0
        falsePos = 0
        trueNeg = neg
        falseNeg = pos
        for row in sortedData:
            if(row[1] == 1):
                truePos += 1
                falseNeg -= 1  
            elif(row[1] == -1):
                falsePos += 1
                trueNeg -= 1
            confusionMatrixList.append(np.array([truePos,falsePos,trueNeg,falseNeg]))
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

        dataTable = np.concatenate([sortedData,confusionMatrix,statisticsArray],1)

        #Save dataframe to file path
        dataFrame = pd.DataFrame(dataTable,columns=['Name','+/-','Score','True Positive', 'False Positive', 'True Negative', 'False Negative', 'Accuracy', 'Precision', 'Recall', 'False Positive Rate', 'Selectivity'])
        dataFrame.to_csv(filePath)




    #Create all gene pairs from an array of single genes
    def makePairs(self,genes):
        pairs = []
        #Loop over all genes
        for i in range(len(genes)):
            #Loop over all genes after gene i
            for j in range(len(genes)-i):
                #Append tuple of gene i and j to pair list
                pairs.append((genes[i],genes[j+i]))
        #Return all pairs as an array
        return np.array(pairs)

    #Creates all pairs of genes that contain atleast 1 positive
    def makePosPairs(self,posGenes,allGenes):
        pairs = []
        for i in range(len(posGenes)):
            for j in range(len(allGenes)):
                pairs.append((posGenes[i],allGenes[j]))
        return(np.array(pairs))
