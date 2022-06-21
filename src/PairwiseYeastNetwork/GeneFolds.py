import pandas as pd
import numpy as np

class GeneFolds():
    def __init__(self,numFolds,posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt'):
        #Reads in lists of positive and negatice genes, then turns each data frame into an array, flattens that array, then turns it into a list
        self.posDataList = pd.read_csv(posGenes).to_numpy().flatten().tolist()
        self.negDataList = pd.read_csv(negGenes).to_numpy().flatten().tolist()

        #Conversts genes lists into gene arrays
        self.posArray = np.array(self.posDataList)
        self.negArray = np.array(self.negDataList)
        #Randomly shuffles gene arrays
        np.random.shuffle(self.posArray)
        np.random.shuffle(self.negArray)

        #posPairs, negPairs, agnPairs = PairwiseYeastData.makePairs(self.posArray,self.negArray,makeAgnositc=True)
        #self.pairs = np.concatenate((posPairs,negPairs,agnPairs))

        self.folds = []
        for i in range(numFolds):
            #Calculate start and end index for positive and negative arrays
            startPos = int(i * len(self.posArray) / numFolds)
            startNeg = int(i * len(self.negArray) / numFolds)
            endPos = int((i+1) * len(self.posArray) / numFolds)
            endNeg = int((i+1) * len(self.negArray) / numFolds)
            #If last fold, go from start position to the end of the each array,
            if (i == numFolds - 1):
                self.folds.append((self.posArray[startPos:],self.negArray[startNeg:]))
            #Otherwise, go to end position
            else:
                self.folds.append((self.posArray[startPos:endPos],self.negArray[startNeg:endNeg]))
    
    #Writes out table of a gene's name, sign, and fold number (counting from 0)
    def writeToCsv(self,path):
        dataTable = []
        #Loops over all folds
        for i in range(len(self.folds)):
            #Gets positive and negative gene arrays and converts them to lists
            posGenes = self.folds[i][0]
            negGenes = self.folds[i][1]
            #Loops over each list, and appends each gene's information
            for gene in posGenes:
                dataTable.append([gene,1,i])
            for gene in negGenes:
                dataTable.append([gene,0,i])
        dataFrame = pd.DataFrame(dataTable,columns=['Gene','+/-','Fold'])
        dataFrame.to_csv(path,index=False)