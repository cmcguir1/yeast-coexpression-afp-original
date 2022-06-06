import torch
from torch.utils.data import Dataset
import pandas as pd
from YeastData import YeastData

class YeastDataset(Dataset):
    def __init__(self,dataArray):
        #Stores data array, includes both features and labels
        self.dataArray = dataArray

    def __getitem__(self,x):
        #Creates a tensor of features, features are all but the first column of data in the data array
        features = torch.from_numpy(self.dataArray[x,1:self.dataArray[x]])
        #Creates a tensor that is a 1 if the gene is in the postive gene set, and a 0 if not
        label = torch.tensor([1 if self.dataArray[x,0] in YeastData.posSet else 0])
        #Return of tuple of the features and label
        return features, label

    def __len__(self):
        #Returns length of data array
        return len(self.dataArray)