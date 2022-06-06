import torch
import pandas as pd
from BostonDataset import BostonDataset
import numpy as np

class BostonData():
    def __init__(self,folds,filePath='./resources/Boston.norm.csv'):
        #Reads in normalized boston data, then shuffles all rows, then converts to nummpy array
        self.data = pd.read_csv(filePath).sample(frac=1).to_numpy()
        self.testingData = self.data[0:int(len(self.data)*0.2)]
        #Creates an empty list, then fills in with equal partitions of the remaining data array
        self.foldedData = []
        for i in range(folds):
            start = int(len(self.data)*0.2 + i*len(self.data)/folds)
            end = int(len(self.data)*0.2 + (i+1)*len(self.data)/folds)
            self.foldedData.append(self.data[start:end])
    
    def getFoldDatasets(self,fold):
        validationSet = BostonDataset(self.foldedData[fold])
        trainingSetArray = np.empty((0,14))
        for i in range(len(self.foldedData)):
            if (i != fold):
                trainingSetArray = np.concatenate((trainingSetArray,self.foldedData[i]),0)
        trainingSet = BostonDataset(trainingSetArray)
        return (trainingSet, validationSet)

