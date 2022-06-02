import readline
import torch
import numpy as np
from IrisModel import IrisModel
from IrisNetworks import IrisNet4x2x3, IrisNet4x3, IrisNet4x3x3x3
from IrisData import IrisData
import pandas as pd

class ModelTester():
    def __init__(self,structure):
        #I am going to write a dictionary that converts a structure string into its associated network
        self.structure = structure
        self.netStructureDict = {'4x3': IrisNet4x3(), '4x2x3': IrisNet4x2x3(), '4x3x3x3': IrisNet4x3x3x3()}
        self.model: IrisModel = IrisModel(network=self.netStructureDict[self.structure])

    #This network resets the model back to a random state with new data
    def resetModel(self):
        self.model.resetModel()

    def testModel(self,runs,epochs,trainP='null',testP='null'):
        #Intialize numpy arrays to store accuracy from each epoch of each run
        trainingDataTable = np.zeros((runs,epochs+1))
        testingDatatable = np.zeros((runs,epochs+1))

        #Loops over the number of runs, training a new network of the same structure
        for run in range(runs):
            #Tests accuracy before the network has been trained
            trainingDataTable[run,0] = self.model.testNetworkAccuracyTraining()
            testingDatatable[run,0] = self.model.testNetworkAccuracyTesting()
            print(f'Run {run}, Epoch {0} Accuracy: {trainingDataTable[run,0]}')
            for epoch in range(epochs):
                #traings network for 1 epoch, then calculates accuracy for training and testing data
                self.model.trainNetwork(1)
                trainingDataTable[run,epoch+1] = self.model.testNetworkAccuracyTraining()
                print(f'Run {run}, Epoch {epoch+1} Accuracy: {trainingDataTable[run,epoch+1]}')
                testingDatatable[run,epoch+1] = self.model.testNetworkAccuracyTesting()
            self.resetModel()

        
        #Creating Column Labels for dataFrames
        colHeaders = []
        for i in range(epochs+1):
            colHeaders.append(f'Epoch {i}')
        #Creates pandas data frame from numpy arrays
        trainingFrame = pd.DataFrame(data=trainingDataTable)
        testingFrame = pd.DataFrame(data=testingDatatable)
        #If no file paths were given, ask the user for location
        if(trainP == 'null' and testP == 'null'):
            #Prompts user for file location, then 
            if(input('Save Data: ') != 'NO'):
                trainingSave = input('Enter training accuracy path: ')
                testingSave = input('Enter testing accuracy path: ')
                trainingFrame.to_csv(trainingSave)
                testingFrame.to_csv(testingSave)
        #Use specified location
        else:
            trainingFrame.to_csv(trainP)
            testingFrame.to_csv(testP)
        

                
