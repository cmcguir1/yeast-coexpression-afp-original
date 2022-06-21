import torch
import numpy as np
import pandas as pd
from FlexNet import FlexNet
from PairwiseModel import PairwiseModel
from PairwiseYeastData import PairwiseYeastData

class YeastGraph(PairwiseModel):
    def __init__(self,networkPath,data,structure,posFile,negFile,agnFile):
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
        #Create gene pairs
        self.pairs = self.makePairs(self.genes)

        #Create a positive gene set from positive gene array
        self.posSet = set(self.posGenes)

        #Make the batch size equal to the number of gene pairs
        self.batch = len(self.pairs)

    #Passes all gene pairs through network, then saves a data table of their outputs
    def feedForward(self,fileLocation,save=True):
        features, labels = self.makeBatchTensors(self.pairs)
        features = features.to(self.device)
        with torch.no_grad():
            outputs = self.net(features)
        self.dataTable = np.array([self.pairs[:,0],self.pairs[:,1],outputs.cpu()]).transpose()
        if(save):
            dataFrame = pd.DataFrame(self.dataTable,columns=['Gene A', 'Gene B', 'Score'])
            dataFrame.to_csv(fileLocation,index=False)

    #Ranks genes by the strength of their connections to positive genes
    def rankGenes(self,filePath):
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
            dataTable.append([gene,scoreDict[gene]])

        #Convert list to array, then sort it by score
        dataArray = np.array(dataTable)
        sortedArray = dataArray[dataArray[:,2].argsort()]
        #Save dataframe to file path
        dataFrame = pd.DataFrame(sortedArray,columns=['Gene','Score'])
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
