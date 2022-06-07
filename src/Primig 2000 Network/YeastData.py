import torch
from pdb import post_mortem
import pandas as pd
import numpy as np

class YeastData():
    #Creates a set of all positive genes to be referenced later
    posFile = pd.read_csv('./Yeast Resources/positives_00_go04-15-07.txt').to_numpy()
    posFile = np.reshape(posFile,(len(posFile)))
    posSet = set()
    for i in posFile:
        posSet.add(i)

    def __init__(self,percentTest,folds,file='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl'):
        #Read in data from file, then drops NAME and GWEIGHT column from the dataFrame, and then converts to numpy array
        self.data = pd.read_csv(file,sep='\t').drop(labels=['NAME','GWEIGHT'],axis=1).to_numpy()
        #Removes first row from numpy array
        self.data = self.data[1:len(self.data)]

        #Dividing entire dataset into positive and negative genes
        posData = []
        negData = []
        #Loops over all genes in dataset
        for gene in self.data:
            #If gene is in the positive set, adds it to the the positive list
            if(gene[0] in YeastData.posSet):
                posData.append(gene)
            #If gene is not in positive set, adds it to the negative list
            else:
                negData.append(gene)
        #Makes numpy arrays of lists and makes them class variables
        self.posData = np.array(posData)
        self.negData = np.array(negData)
        #Shuffles contents of arrays
        np.random.shuffle(self.posData)
        np.random.shuffle(self.negData)


        #Variables for the percentage of data that will be folded
        self.percentTest = percentTest
        self.folds = folds

        #Takes the first percentTest percent of posData and negData, concatenates those arrays together, then makes a test dataset out of them
        #Note that we can can make this a single data set because this data will only ever be used to test, and thus does not require and equal parition of positive and negative examples
        # testPos = self.posData[0:int(len(self.posData)*self.percentTest)]
        # testNeg = self.negData[0:int(len(self.negData)*self.percentTest)]
        # self.testingData = np.concatenate([testPos,testNeg],0)

        #Calculates the portion of the dataset each fold should contain
        foldPart = len(self.posData)*(1-percentTest)
        self.partitions = []
        testStart = 0 #testStart will eventually store the value of the end of the last fold
        for i in range(folds):
            #Uses foldPart to calculate what part of the data array each partition will contain
            posPartition = self.posData[i*int(foldPart/self.folds):(i+1)*int(foldPart/self.folds)]
            negPartition = self.posData[i*int(foldPart/self.folds):(i+1)*int(foldPart/self.folds)]
            #Appends a tuple of the positive and negative partitions to the partitions list
            self.partitions.append((posPartition,negPartition))
            #On the last partition, store the testStart index
            if(i == folds - 1):
                testStart = (i+1)*int(foldPart/self.folds)
        
        #Take what is leftover from fold partitions from positive and negative datasets, then concats them together into testing array
        testPos = self.posData[testStart:-1]
        testNeg = self.negData[testStart:-1]
        self.testingData = np.concatenate([testPos,testNeg])

    def getFold(self,x):
        #Creates an empty array for the pos and negative partitions
        posRet = np.zeros((0,len(self.partitions[0][0][0])))
        negRet = np.zeros((0,len(self.partitions[0][1][0])))
        #Loops over the partitions list and adds non validation partitions into each respecitve return array
        for i in range(len(self.partitions)):
            if(i != x):
                #partitions is a list of tuples, so we need to unpack
                posPart, negPart = self.partitions[i]
                posRet = np.concatenate((posRet,posPart))
                negRet = np.concatenate((negRet,negPart))
        #Creates return arrays for the validation data set based on specified index
        posVal, negVal = self.partitions[x]

        #Returns a list of [postive training, negative training, positive validation, negative validation]
        return (posRet,negRet,posVal,negVal)

        
    
