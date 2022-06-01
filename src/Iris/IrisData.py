from isort import file
import torch
import pandas as pd
import numpy as np
from IrisDataset import IrisDataset

class IrisData():
    def __init__(self,percentTraining,filePath,stratified=True):
        #Defaults to making the training and testing datasets stratified unless
        if(stratified):
            #Load iris data in from csv file and convert it to numpy array
            dataArray = pd.read_csv(filePath).to_numpy()
            #Splice the dataArray to make seperate array for each species of Iris
            setosaArray = dataArray[0:50].copy()
            versicolorArray = dataArray[50:100].copy()
            viginicaArray = dataArray[100:150].copy()
            #Shuffle all rows for each array of species data
            np.random.shuffle(setosaArray)
            np.random.shuffle(versicolorArray)
            np.random.shuffle(viginicaArray)
            #Concatonate the first percentTraining percentage of each species array together to send to training data
            trainingDataArray = np.concatenate((setosaArray[0:int(len(setosaArray)*percentTraining)],versicolorArray[0:int(len(versicolorArray)*percentTraining)],viginicaArray[0:int(len(viginicaArray)*percentTraining)]))
            testingDataArray = np.concatenate((setosaArray[int(len(setosaArray)*percentTraining):len(setosaArray)],versicolorArray[int(len(versicolorArray)*percentTraining):len(setosaArray)],viginicaArray[int(len(viginicaArray)*percentTraining):len(setosaArray)]))
            #Initialize training and testing data sets using array from above
            self.trainingData = IrisDataset(trainingDataArray)
            self.testingData = IrisDataset(testingDataArray)
        else:
            #read in iris data csv and shuffle order, then convert to numpy array
            dataArray = pd.read_csv(filePath).sample(frac=1).to_numpy()
            #The full random iris data is then split between a training and testing set based on the percentTraining
            self.trainingData = IrisDataset(dataArray[0:int(percentTraining*len(dataArray))])
            self.testingData = IrisDataset(dataArray[int(percentTraining*len(dataArray)):len(dataArray)])

    #Test mtehod to check if the data is stratified
    def printDataSets(self):
        print(self.trainingData)
        print(self.testingData)

        




