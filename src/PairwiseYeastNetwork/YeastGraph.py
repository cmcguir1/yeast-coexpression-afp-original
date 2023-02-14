
import torch
import numpy as np
import pandas as pd
from FlexNet import FlexNet
from PairwiseModel import PairwiseModel
from PairwiseYeastData import PairwiseYeastData
import time
import os


class YeastGraph(PairwiseModel):
    def __init__(self,networkPath,data,structure,posFile,negFile,agnFile,folder,includeAll=True,numfolds=4):
        #Intialize PairwiseYeastData as data
        self.data : PairwiseYeastData = data

        #Initializes path where data will be saved
        self.path = f'./Yeast Resources/GraphResults/{folder}'
        #If the folder does not already exist, create it
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        pd.DataFrame(['Test File']).to_csv(f'{self.path}/TestFile.csv',index=False,header=False)

        self.numFolds = numfolds
    
        #Creates a list of networks, each which trained on a different fold
        print('Starting to Initialize Networks')
        self.nets = []
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        for i in range(numfolds):
            net = FlexNet(structure=structure)
            net.load_state_dict(torch.load(f'{networkPath}{i+1}.pth'))
            net.to(self.device)
            self.nets.append(net)

        #Intialize pos, neg, and agn gene arrays, then concatentate them together
        print("Initializing genes")
        posTrain,negTrain,posVal,negVal = self.data.getFold(0)

        self.posGenes = np.concatenate([posTrain,posVal])
        self.negGenes = pd.read_csv(negFile).to_numpy().flatten()
        self.agnGenes = pd.read_csv(agnFile).to_numpy().flatten()

        self.genes = np.concatenate([self.posGenes,self.negGenes,self.agnGenes],0)
        print(f'Number of Genes: {len(self.genes)}')
        #If includeAll is true, make every gene pair
        if(includeAll):
            self.pairs = self.makePairs(self.genes)
        #Otherwise, only make gene pairs that include at least 1 positive
        else:
            self.pairs = self.makePosPairs(self.posGenes,self.genes)

        

        #Create a positive gene set from positive gene array
        self.posSet = set(pd.read_csv(posFile).to_numpy().flatten())
        self.agnSet= set(self.agnGenes)
        self.negSet = set(self.negGenes)

        #Make agnostic pairs for feed forward
        self.agnPairs = self.makePosPairs(self.agnGenes,self.posGenes)

        #Make the batch size equal to the number of gene pairs
        self.batch = len(self.pairs)

    #Passes all gene pairs through network, then saves a data table of their outputs
    def feedForward(self,fileLocation,save=True,fold=None,limitPairs=None):
        self.limitPiars = limitPairs
        #If a no fold is specified, calculate all folds, then combine them together into one file
        if fold == None:
            #This should be restructures to let you pick a network to feed forward so it can be parallelized
                
            folds = []
            agnFolds = []
            for i, net in enumerate(self.nets,0):
                outputTable, agnTable = self.forward(net,i)
                folds.append(outputTable)
                agnFolds.append(agnTable)

            #Take all agnostic scores and average them for each pair
            agnAverage = []
            agnPairs = self.agnPairs
            for i in range(len(agnPairs)):
                #For every fold, add the score of a given pair to total
                total = 0
                for table in agnFolds:
                    total += table[i,2]
                #Append the average
                agnAverage.append([agnPairs[i,0],agnPairs[i,1],total/self.numFolds])
            agnAverageArray = np.array(agnAverage)

            #Append agnostic data to folds, then concatenate all folds together to create the full dataTable
            folds.append(agnAverageArray)
            self.dataTable = np.concatenate(folds,0)
            if(save):
                pd.DataFrame(self.dataTable,columns=['Gene A','Gene B','Score']).to_csv(f'{self.path}/{fileLocation}')
        
        #Otherwise, only calculate that fold
        else:
            self.forward(self.nets[fold],fold)
        
    def forward(self,net,fold):
        with torch.no_grad():  
    

            #Loop over all networks, for each network, feed forward all gene pairs from the validation fold assocaited with that network
            #Get the gene data from fold of network i
            posTrain,negTrain,posVal,negVal = self.data.getFold(fold)
            #Make pairs between positive genes and all genes from fold
            posPairs = self.makePosPairs(posVal,np.concatenate([posVal,posTrain]))
            negPairs = self.makePosPairs(negVal,np.concatenate([posVal,posTrain]))
            agnPairs = self.agnPairs
            pairs = np.concatenate([posPairs,negPairs,agnPairs],0)

            #Feed positive pairs through netowrk
            outputsList = []
            for i, pair in enumerate(pairs,0):
                #Make features tensor from single pair
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                #Append output to outputs list
                outputsList.append(net(features.float(),test=True).cpu().flatten()[0])
                if(i % 100 == 0):
                     print(f'Pairs Calculated: {(i+1)/len(pairs)}%',flush=True)
            #Convert outputsList to array, then make take of gene 1, gene 2, score
            outputs = np.array(outputsList)
            outputsTable = np.array([pairs[:,0],pairs[:,1],outputs],dtype=object).transpose()
            #Save positives pairs to csv file
            pd.DataFrame(outputsTable,columns=['Gene A','Gene B','Score']).to_csv(f'{self.path}/PosPairsFold{fold+1}.csv',index=False)

            #Get all agnositc apirs
            agnPairs = self.agnPairs
            agnOutputsList = []
            #Feed all agnositc pairs through network
            for i, pair in enumerate(agnPairs,0):
                #Make features tensor from single pairS
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                #Feed pair through network
                agnOutputsList.append(net(features.float(),test=True).cpu().flatten()[0])
                if(i % 100 == 0):
                     print(f'Pairs Calculated (Agnostic): {(i+1)/len(agnPairs)}%',flush=True)
            #Make agnostic pair table, then append it to agnostic folds list
            agnOutputs = np.array(agnOutputsList)
            agnOutputsTable = np.array([agnPairs[:,0],agnPairs[:,1],agnOutputs],dtype=object).transpose()
            #Saves agnostic pairs to csv file
            pd.DataFrame(agnOutputsTable,columns=['Gene A','Gene B','Score']).to_csv(f'{self.path}/AgnPairsFold{fold+1}.csv',index=False)
            
            #return (outputsTable,agnOutputsTable)
    
    def recombineFolds(self,posPath,agnPath,fileLocation,numFolds=4):
        folds = []
        agnFolds = []
        for i in range(numFolds):
            folds.append(pd.read_csv(f'{self.path}/{posPath}{i+1}.csv').to_numpy(dtype=object))
            agnFolds.append(pd.read_csv(f'{self.path}/{agnPath}{i+1}.csv').to_numpy(dtype=object))

        agnAverage = []
        agnPairs = self.agnPairs
        for i in range(len(agnPairs)):
            #For every fold, add the score of a given pair to total
            total = 0.0
            for table in agnFolds:
                #print(table)
                total += table[i,2]
            #Append the average
            agnAverage.append([agnPairs[i,0],agnPairs[i,1],total/float(self.numFolds)])
        agnAverageArray = np.array(agnAverage,dtype=object)

        folds.append(agnAverageArray)

        self.dataTable = np.concatenate(folds,0)
        pd.DataFrame(self.dataTable,columns=['Gene A','Gene B','Score']).to_csv(f'{self.path}/{fileLocation}',index=False)

   #Compare the performance of each net on gene pairs from genes that fold of data
    def compareFolds(self,saveLoc,cutoff=100):
        pairTable = []
        for i in range(self.numFolds):
            posTrain,negTrain,posVal,negVal = self.data.getFold(i)
            np.random.shuffle(posVal)
            pairs = self.makePosPairs(posVal,np.concatenate([posTrain,negTrain,posVal,negVal]))
            np.random.shuffle(pairs)
            pairs = pairs[:cutoff]
            for pair in pairs:
                pairResults = [pair[0],pair[1],i]
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                worst = 0.0
                worstIndex = 0
                for j,net in enumerate(self.nets,0):
                    output = net(features.float(),test=True).cpu().flatten().item()
                    if j == 0:
                        worst = output
                        worstIndex = j
                    elif output < worst:
                        worst = output
                        worstIndex = j
                    pairResults.append(output)
                pairResults.append(worstIndex)
                pairTable.append(pairResults)
        total = 0
        fold0 = 0
        fold1 = 0
        fold2 = 0
        fold3 = 0
        for row in pairTable:
            if row[2] == row[7]:
                total += 1
            if row[7] == 0:
                fold0 += 1
            elif row[7] == 1:
                fold1 += 1
            elif row[7] == 2:
                fold2 += 1
            else:
                fold3 += 1
        print(f'Pairs: {total} / {len(pairTable)}')
        print(f'Fold0 worst predictions: {fold0} / {len(pairTable)}')
        print(f'Fold1 worst predictions: {fold1} / {len(pairTable)}')
        print(f'Fold2 worst predictions: {fold2} / {len(pairTable)}')
        print(f'Fold3 worst predictions: {fold3} / {len(pairTable)}')

        pd.DataFrame(pairTable,columns=['Gene A','Gene B','Fold #','Fold 0 Prediction','Fold 1 Prediction','Fold 2 Prediction','Fold 3 Prediction','Lowest Confidence']).to_csv(saveLoc,index=False)

                
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
            if genePair[0] != genePair[1]:

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
        dataFrame.to_csv(f'{self.path}/{filePath}',index=False)

    


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

    #Take in positive gene files for mito inheritance and another GO term and compare the a certain number of random gene pairs from each set
    def compareGOTerms(self,mitoPos,otherPos,cutoff=1000):
        mitoPairs = self.makePairs(pd.read_csv(mitoPos).to_numpy().flatten())
        otherPairs = self.makePairs(pd.read_csv(otherPos).to_numpy().flatten())
        mixedPairs = self.makePosPairs(pd.read_csv(mitoPos).to_numpy().flatten(),pd.read_csv(otherPos).to_numpy().flatten())
        np.random.shuffle(mitoPairs)
        np.random.shuffle(otherPairs)
        np.random.shuffle(mixedPairs)
        mitoPairs = mitoPairs[:cutoff]
        otherPairs = otherPairs[:cutoff]
        mixedPairs = mixedPairs[:cutoff]
        with torch.no_grad():
            mitoTotal = 0.0
            for pair in mitoPairs:
                features,_ = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                for net in self.nets:
                    output = net(features.float(),test=True).cpu().flatten().item()
                    mitoTotal += output
            otherTotal = 0.0
            for pair in otherPos:
                features,_ = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                for net in self.nets:
                    output = net(features.float(),test=True).cpu().flatten().item()
                    otherTotal += output
            mixedTotal = 0.0
            for pair in mixedPairs:
                features,_ = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                for net in self.nets:
                    output = net(features.float(),test=True).cpu().flatten().item()
                    mixedTotal += output
        print(f'Average Mitochondrial Inheritance Confidence: {mitoTotal/(len(mitoPairs)*len(self.nets))}')
        print(f'Average Other GO Term Confidence: {otherTotal/(len(otherPairs)*len(self.nets))}')
        print(f'Average Mixed Pair Confidence: {mixedTotal/(len(mixedPairs)*len(self.nets))}')

    #This method divides a pairs file into a file for positive pairs and a file for negative pairs
    def dividePosNeg(self,pairsFile):
        pairs = pd.read_csv(pairsFile).to_numpy()
        posPairs = []
        negPairs = []
        for pair in pairs:
            if pair[0] in self.posSet and pair[1] in self.posSet:
                posPairs.append(pair)
            elif (pair[0] in self.negSet and pair[1] in self.negPos) or (pair[0] in self.posSet and pair[1] in self.negSet):
                negPairs.append(pair)
        saveLoc = pairsFile[0:pairsFile.rfind('.')]
        pd.DataFrame(posPairs,columns=['Gene A','Gene B','Score']).to_csv(f'{saveLoc}_PosPairs.csv',index=False)
        pd.DataFrame(negPairs,columns=['Gene A','Gene B','Score']).to_csv(f'{saveLoc}_NegPairs.csv',index=False)

    def compareOverFitting(self,fold,saveLoc,cutoff=1000):
        posTrain, negTrain, posVal, negVal = self.data.getFold(fold)
        posPairs = self.makePairs(posVal)
        negPairs = self.makePosPairs(posVal,np.concatenate([posTrain,negTrain,negVal]))
        pairs = np.concatenate([posPairs,negPairs],0)
        np.random.shuffle(pairs)
        with torch.no_grad():
            for i,net in enumerate(self.nets,0):
                dataTable = []
                for pair in pairs:
                    features,_ = self.makeBatchTensors(np.array([pair]))
                    features = features.to(self.device)
                    output = net(features.float(),test=True).cpu().flatten().item()
                    dataTable.append([pair[0],pair[1],output])
                pd.DataFrame(dataTable,columns=['Gene A','Gene B','Score']).tocsv(f'{saveLoc}_fold{fold+1}_Pairs_Net{i+1}.csv')
                self.rankGenes(f'{saveLoc}_fold{fold+1}_Ranked_Net{i+1}.csv',dataTablePath=f'{saveLoc}_fold{fold+1}_Pairs_Net{i+1}.csv')

    def filterAgn(self,filePath):
        table = pd.read_csv(filePath).to_numpy()
        filteredTable = []
        for genePair in table:
            if not(genePair[0] in self.agnSet):
                filteredTable.append(genePair)
        pd.DataFrame(filteredTable,columns=['Gene A','Gene B','Score']).to_csv(filePath,index=False)

    def saveGenesToCSV(self,location):
        pd.DataFrame(self.genes).to_csv(location,index=False)

