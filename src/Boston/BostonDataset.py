import torch
from torch.utils.data import Dataset
import numpy as np

#Dataset class for Boston Data
class BostonDataset(Dataset):
    #Initialized data array
    def __init__(self,dataArray):
        self.dataArray = dataArray
    
    #Returns the a tuples of a tensor of features and a tensor of labels at a given index
    def __getitem__(self,idx):
        features = torch.from_numpy(np.delete(self.dataArray,13,1)[idx])
        labels = torch.tensor([self.dataArray[idx,13]])
        return features, labels

    #Returns length of dataset
    def __len__(self):
        return len(self.dataArray)