import pandas as pd
import numpy as np

class GeneFolds():
    def __init__(numFolds,self,posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt'):
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
                self.folds.append((set(self.posArray[startPos:]),set(self.negArray[startNeg:])))
            #Otherwise, go to end position
            else:
                self.folds.append((set(self.posArray[startPos:endPos]),set(self.negArray[startNeg:endNeg])))
    
    def writeToCsv(self):
        dataTable = []
        for i in range(self.folds):
            i