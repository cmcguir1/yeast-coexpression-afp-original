import pandas as pd
import numpy as np
from BostonModel import BostonModel
from torch.utils.data import DataLoader
from BostonDataset import BostonDataset

from BostonData import BostonData

class CrossValidator():
    def __init__(self,folds,networkType,batch_size=4,filePath='./resources/Boston.norm.csv'):
        #Number of folds the training data is divided into
        self.folds = folds
        self.batch_size = batch_size
        #Boston data set divided up into a specified number of folds, and a set of testing data
        self.data = BostonData(self.folds,filePath)
        #Retrive testing data used later for cross validation and create a b
        testingData = BostonDataset(self.data.testingData)
        self.testingLoader = DataLoader(testingData,batch_size=self.batch_size,shuffle=True,num_workers=2)
        
        #Creates a list of models that each uses a different fold of the dataset
        self.models = []
        for i in range(folds):
            trainLoad, valLoad = self.data.getFoldDatasets(i)
            self.models.append(BostonModel(trainLoad,valLoad,networkType,batch_size=self.batch_size))

    def crossValidate(self,epochs,fileName='null'):
        #Creates a data table for each folds, the plus 1 is for the untrained model
        dataTable = np.zeros((self.folds*3,epochs+1))
        #Loop over all models of different folds
        for i in range(len(self.models)):
            #Test each model when it is untrained
            dataTable[i*3,0] = self.models[i].testNetworkTrain()
            dataTable[(i*3)+1,0] = self.models[i].testNetworkVal()
            dataTable[(i*3)+2,0] = self.models[i].testNetwork(self.testingLoader)
            
            #Loop over the number of epochs for each model
            for epoch in range(epochs):
                #Train network once, then test its accuracy on training, validation, and testing data
                self.models[i].trainNetwork(1)
                dataTable[i*3,epoch+1] = self.models[i].testNetworkTrain()
                dataTable[(i*3)+1,epoch+1] = self.models[i].testNetworkVal()
                dataTable[(i*3)+2,epoch+1] = self.models[i].testNetwork(self.testingLoader)
                print(f'Epoch {epoch+1}')
            print(f'Finished Model {i+1}')
        #Convert the numpy array data table into a pandas dataframe
        dataFrame = pd.DataFrame(dataTable)
        print(dataFrame)
        #If user did not specify a  file name, prompt them for one
        if(fileName == 'null'):
            name = input('What is the name of this file: ')
            dataFrame.to_csv(f'./resources/{name}')
        else:
            dataFrame.to_csv(f'./resources/{fileName}')

