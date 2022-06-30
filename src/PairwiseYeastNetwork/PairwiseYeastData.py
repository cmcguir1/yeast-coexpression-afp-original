import glob
from YeastDataFile import YeastDataFile
import pandas as pd
import numpy as np
import time as time
from ExpressionDatasets import ExpressionDatasets

class PairwiseYeastData():
    def __init__(self,folder,numFolds,foldFile='',filterMissingGenes=False,sort=True,recalc=False,statsDictLoc='',numDatasets=50,subset=100000,recur=True,posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt'):

        #Reads in lists of positive and negatice genes, then turns each data frame into an array, flattens that array, then turns it into a list
        self.posDataList = pd.read_csv(posGenes).to_numpy().flatten().tolist()
        self.negDataList = pd.read_csv(negGenes).to_numpy().flatten().tolist()
        #Set of all positive genes
        self.posDataSet = set(self.posDataList)

        #Conversts genes lists into gene arrays
        self.posArray = np.array(self.posDataList)
        self.negArray = np.array(self.negDataList)
        #Randomly shuffles gene arrays
        np.random.shuffle(self.posArray)
        np.random.shuffle(self.negArray)

        #Generate all possible gene pairs, concatentate them into one array
        #This array is used to calculate the mean and std of each dataset

        posPairs, negPairs, agnPairs = PairwiseYeastData.makePairs(self.posArray,self.negArray,makeAgnositc=True)
        pairs = np.concatenate((posPairs,negPairs,agnPairs))

        
        self.expression = ExpressionDatasets(numDatasets,folder,pairs,subset,sort,recur,recalc,statsDictLoc)
        self.datasets = self.expression.datasets
        
        if(filterMissingGenes):
            self.filterGenes()
            #Conversts genes lists into gene arrays
            self.posArray = np.array(self.posDataList)
            self.negArray = np.array(self.negDataList)
            #Randomly shuffles gene arrays
            np.random.shuffle(self.posArray)
            np.random.shuffle(self.negArray)



        #Intializes empty list that will hold each fold of data, each fold will be a tuple of (pos data, neg data)
        #Each fold of the data will contain a tuple of a set of positive genes and a set of negative genes
        self.folds = []
        if(not(foldFile == '')):
            foldData = pd.read_csv(foldFile).to_numpy()
            posList = []
            negList = []
            for i in range(numFolds):
                posList.append(set())
                negList.append(set())
            for gene in foldData:
                if(gene[1] == 1):
                    posList[gene[2]].add(gene[0])
                else:
                    negList[gene[2]].add(gene[0])
            for i in range(numFolds):
                self.folds.append((posList[i],negList[i]))

        else:
            for i in range(numFolds):
                #Calculate start and end index for positive and negative arrays
                startPos = int(i * len(self.posArray) / numFolds)
                startNeg = int(i * len(self.negArray) / numFolds)
                endPos = int((i+1) * len(self.posArray) / numFolds)
                endNeg = int((i+1) * len(self.negArray) / numFolds)
                #If last fold, go from start position to the end of the each array,
                if (i == numFolds - 1):
                    self.folds.append((set(self.posArray[startPos:]),set(self.negArray[startNeg:])))
                #Otherwise, go to end position
                else:
                    self.folds.append((set(self.posArray[startPos:endPos]),set(self.negArray[startNeg:endNeg])))

    #Returns a specified fold as validation data, and the other folds as training data
    def getFold(self,fold):
        #Makes lists of positive and negative training folds, then concatentates them together
        posTrainList  = []
        negTrainList = []
        for i in range(len(self.folds)):
            if(i != fold):
                posTrainList.append(list(self.folds[i][0]))
                negTrainList.append(list(self.folds[i][1]))
        posTrain = np.concatenate(posTrainList)
        negTrain = np.concatenate(negTrainList)
        #Gets validation data from specified fold
        posVal, negVal = list(self.folds[fold][0]), list(self.folds[fold][1])
        #Returns data as a tuple
        return (posTrain,negTrain,posVal,negVal)

    #This method filters out any genes that are not found in all datasets, because this may cause a problem when training a network
    def filterGenes(self):
        #Initializes empty sets that will hold genes that need to be removed
        posRemove = set()
        negRemove = set()
        #For all positive and negative genes, loops over all dataset dictionaries, and adds gene to repsective remove set if gene is not found in any dictionary
        for gene in self.posDataList:
            for dataset in self.datasets:
                if(not(gene in dataset.geneDict)):
                    posRemove.add(gene)
        for gene in self.negDataList:
            for dataset in self.datasets:
                if(not(gene in dataset.geneDict)):
                    negRemove.add(gene)
        #Removes genes from remove lists from data lists
        for gene in posRemove:
            self.posDataList.remove(gene)
        for gene in negRemove:
            self.negDataList.remove(gene)

    #Takes in arrays of positive and negative genes, and returns arrays of all positive and negative genes pairs
    def makePairs(posGenes,negGenes,makeAgnositc=False):
        posGenePairs = []
        #Loops over a genes in posGenes
        for i in range(len(posGenes)):
            #Loops over all other remaining genes after gene i
            for j in range(i+1,len(posGenes)):
                #Appends a tuple of (gene i, gene j) to positive gene pairs list
                posGenePairs.append((posGenes[i],posGenes[j]))
        #This section of code does the same thing but for negative genes
        negGenePairs = []
        for i in range(len(negGenes)):
            for j in range(i+1,len(negGenes)):
                negGenePairs.append((negGenes[i],negGenes[j]))
        #If makeAgnostic is true, adds all pairs of positive and negative genes to agnostic pair list, then returns all gene pairs
        if(makeAgnositc):
            agnGenePairs = []
            for i in range(len(posGenes)):
                for j in range(len(negGenes)):
                    agnGenePairs.append((posGenes[i],negGenes[j]))
            return (np.array(posGenePairs),np.array(negGenePairs),np.array(agnGenePairs))
        #If not, then only return positive pairs and negative pairs
        else:
            return (np.array(posGenePairs),np.array(negGenePairs))

    #Calculates correlation coefficent between all gene pairs for all datasets, this is used to generate hisogram distributions of pearson correlation for a dataset
    def calculateCorrelations(self):
        #Creates positive, negative, and agnostic gene pairs
        posPairs, negPairs, agnPairs = PairwiseYeastData.makePairs(self.posArray,self.negArray,makeAgnositc=True)
        #Loop over all datasest
        for dataset in self.datasets:
            #Create empty dataTable list
            dataTable = []
            #Loop over all gene pairs in each array, and calculate correlation coefficent, then add all information to list
            for genePair in posPairs:
                dataTable.append([genePair[0],genePair[1],'P-P',np.corrcoef(dataset.geneDict[genePair[0]],dataset.geneDict[genePair[1]])[1,0]])
            for genePair in negPairs:
                dataTable.append([genePair[0],genePair[1],'P-N',np.corrcoef(dataset.geneDict[genePair[0]],dataset.geneDict[genePair[1]])[1,0]])
            for genePair in agnPairs:
                dataTable.append([genePair[0],genePair[1],'N-N',np.corrcoef(dataset.geneDict[genePair[0]],dataset.geneDict[genePair[1]])[1,0]])
            #Turn list into dataframe
            dataFrame = pd.DataFrame(dataTable,columns=['Gene A', 'Gene B', 'Type', 'Correlation'])
            #Uses string methods to isolate part of the file name we want for saving the dataframe
            #.rfind() finds last occurance of character
            fileName = dataset.dataFile[dataset.dataFile.find('\\')+1:dataset.dataFile.rfind('.')]
            dataFrame.to_csv(f'./Yeast Resources/Histogram Data/Corr_{fileName}.csv',index=False)

    #Method that saves all calculated statisitcs for each datast to a csv file, this csv file is used to make a statisitcs dictionary in another function
    def saveStatistics(self,location):
        dataTable = []
        for dataset in self.datasets:
            dataTable.append([dataset.dataFile,dataset.mean,dataset.std])
        dataFrame = pd.DataFrame(dataTable,columns=['File Name', 'Mean', 'Standard Deviation'])
        dataFrame.to_csv(location,index=False)

    #Function that reads in a csv file, then creates a dictionary with file name keys and (mean,std) values
    def makeStatsDict(self,fileName):
        dataTable = pd.read_csv(fileName).to_numpy(dtype=object)
        geneDict = {}
        for row in dataTable:
            geneDict[row[0]] = (row[1],row[2])
        return geneDict
            



    