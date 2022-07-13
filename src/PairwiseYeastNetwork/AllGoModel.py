import pandas as pd
import numpy as np
from FlexNet import FlexNet
from ExpressionDatasets import ExpressionDatasets
import torch

import sys
from YeastDataFile import YeastDataFile

sys.path.insert(0,'./obopy')
from Leaf import getLeaves


class AllGoModel():
    def __init__(self,fold,foldFile,structure,saveLocation,modelName,lr=0.01,momentum=0.9,batch=50):
        #Read in file of gene folds
        folds = pd.read_csv(foldFile).to_numpy()
        
        #Loop over all genes in folds
        val = []
        train = []
        for gene in folds:
            #If gene's fold matches fold variable, add to validation list
            if gene[1] == fold:
                val.append(gene[0])
            #Otherwise, add ot training list
            else:
                train.append(gene[0])
        #Make instance varaibles of array of training genes and array of validation genes
        self.training = np.array(train)
        self.validation = np.array(val)


        #getLeaves returns a list of tuple of (GO Term,{set of genes})
        self.leaves = getLeaves(10)

        
        #Initialize all expression data as a list of maps {gene -> expression array}
        self.datasets = ExpressionDatasets('./Yeast Resources/Datasets/all spell datasets').datasets


        #Initialize the network, the size of the input layer is the number of expression datasets, and the size of the output is the number of leaf go terms
        struct = f'{len(self.datasets)}x{structure}x{len(self.leaves)}'
        self.net = FlexNet(struct,sigmoid=False)
        #Choose which device to run network on, then move network to that device
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)


        #Initialize Loss function, we are using CEL because we have multiple outputs that could be true
        self.lossFunc = torch.nn.CrossEntropyLoss()
        #Stochastic Gradient Descent Optimizer
        self.opt = torch.optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)
        #Instance variable for batch size
        self.batch = batch
        self.fold = fold

        #Locations to save all output data
        self.networkLoc = f'./Yeast Resources/Pairwise/Spell/{saveLocation}/{modelName}_{struct}_Net_fold{self.fold+1}.csv'
        self.lossLoc = f'./Yeast Resources/Pairwise/Spell/{saveLocation}/{modelName}_{struct}_Loss_fold{self.fold+1}.csv'
        self.trainLoc = f'./Yeast Resources/Pairwise/Spell/{saveLocation}/{modelName}_{struct}_Train_fold{self.fold+1}.csv'
        self.testLoc = f'./Yeast Resources/Pairwise/Spell/{saveLocation}/{modelName}_{struct}_Test_fold{self.fold+1}.csv'

    def trainNetwork(self,epochs):
        #Initialize all pairs of training genes
        pairs = self.makePairs(self.training)

        runningLoss = 0.0
        lossList = []
        #Run training loop epochs number of times
        for epoch in range(epochs):
            #Reset gradients before running each training step
            self.opt.zero_grad()
            
            #Make batch array of gene pairs
            batchArray = self.makeBatchArray(pairs)
            #Make features and labels tensors from batcharray
            features, labels = self.makeBatchTensors(batchArray)
            #Move both tensors to device of model
            feautures = features.to(self.device)
            labels = labels.to(self.device)

            outputs = self.net(features.float())
            loss = self.lossFunc(outputs.float(),labels.float())
            runningLoss += loss
            loss.backward()
            self.opt.step()
            
            if epoch % 100 == 0 and epoch != 0:
                lossList.append(runningLoss)
                runningLoss = 0.0
                pd.DataFrame(lossList,columns=['Loss']).to_csv(self.lossLoc,index=False)
        self.net._save_to_state_dict(self.networkLoc)
            
            

    #Makes input batches with gene names
    def makeBatchArray(self,pairs):
        #Returns array with batch size number of random gene pairs
        return pairs[np.random.choice(len(pairs),self.batch,replace=False),:]

    def makeBatchTensors(self,batchArray):
        featureList = []
        labelsList = []
        #Loop over all gene pairs in the batcharray
        for genePair in batchArray:
            corrList = []
            #Calculate correlation coefficients for each dataset
            for dataset in self.datasets:
                rho = dataset.customCorrelation(genePair)
                #Adjust rho if 1 or -1 because of problems with fisher z transform
                if rho == 1:
                    rho = 0.99
                elif rho == -1:
                    rho = -0.99
                corrList.append(rho)
            featureList.append(corrList)

            #Loop over all GO terms in slim
            for leaf in self.leaves:
                label = []
                #If both genes are annotated to that GO term, append 1 to label list
                if genePair[0] in leaf[1] and genePair[1] in leaf[1]:
                    label.append(1)
                #Otherwise, append 0
                else:
                    label.append(0)
            labelsList.append(label)

        #Convert both list to tensors, then return them as a tuple
        featureTensor = torch.tensor(featureList)
        labelsTensor = torch.tensor(labelsList)
        return (featureTensor,labelsTensor)
        

        


    #Returns array of all pairs of gene from given array of genes
    def makePairs(self,genes):
        pairs = []
        #Loop over all genes
        for i in range(len(genes)):
            #Loop over all genes after gene i
            for j in range(i,len(genes)):
                #Append a tuple of (gene i, gene j)
                pairs.append((genes[i],genes[j]))
        return np.array(pairs)

        







