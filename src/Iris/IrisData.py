import torch
import pandas as pd
import numpy as np
from IrisDataset import IrisDataset

class IrisData():
    def __init__(self,percentTraining,filePath):
        #read in iris data csv and shuffle order, then convert to numpy array
        dataArray = pd.read_csv(filePath).sample(frac=1).to_numpy()
        #The full random iris data is then split between a training and testing set based on the percentTraining
        self.trainingData = IrisDataset(dataArray[0:int(percentTraining*len(dataArray))])
        self.testingData = IrisDataset(dataArray[int(percentTraining*len(dataArray)):len(dataArray)])
