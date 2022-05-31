import torch
from torch.utils.data import Dataset
import csv
import pandas as pd
import numpy as np

#This class will be the dataset for our Iris data

class IrisDataset(Dataset):
    def __init__(self,dataArray):
        #Intializes labels as the 4th column of the dataArray
        self.labels = torch.from_numpy(dataArray[:,4]) #1D Tensor of strings, Iris labels
        self.features = torch.from_numpy(np.delete(dataArray,4,1)) #2D Tensor of doubles, Iris features

        #Dictionary that maps species name to a number
        self.speciesToNumber = {'Iris-vericolor': 0, 'Iris-setosa': 1, 'Iris-virginica':2}

    def __getitem__(self,idx):
        #For now, I think I am going to maps species name to a number
        
        #Creates tensor of 0's, then makes creates an output tensor based on the species of an iris of a given idx
        tempLabel = torch.zeros(3)
        tempLabel[self.speciesToNumber(self.labels[idx])] = 1

        #Creates return tensor that is the features of an iris at a given idx
        tempFeature = self.features[idx]

        return tempFeature, tempLabel

    def __len__(self):
        return len(self.labels)

