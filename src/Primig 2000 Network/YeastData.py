from YeastDataset import YeastDataset
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
        testPos = self.posData[0:int(len(self.posData)*self.percentTest)]
        testNeg = self.negData[0:int(len(self.negData)*self.percentTest)]
        self.testingData = YeastDataset(np.concatenate((testPos,testNeg)))

        #Make the testing data the last part of a the data array
        self.partitions = []
        for i in range(folds):
            # posPartition = self.posData[int(len(self.posData)*self.percentTest + (i)*):]
            # negPartition = 
            self.partitions.append(())

