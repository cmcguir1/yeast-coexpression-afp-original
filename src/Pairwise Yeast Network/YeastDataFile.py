from cProfile import label
import pandas as pd
import numpy as np
import time

#Takes a filePath, then creates a gene dictionary
class YeastDataFile():
    def __init__(self,filePath,pairs,subset):
        #Reads in file from filePath, expected to be tab delimited, then drops the NAME and GWEIGHT columns can converts to numpy
        self.data = pd.read_csv(filePath,sep='\t').drop(labels=['NAME','GWEIGHT'],axis=1).to_numpy()
        #Removes first row from data array as it will always be the number 1
        self.data = self.data[1:]

        #dataFile stores the name of the data file, including which folder the file is found within Yeast Resources
        self.dataFile = filePath[filePath.find('Yeast Resources/')+15:]

        #Intializes an empty gene dictionary that will take in a gene in return its expression data for this dataset
        self.geneDict = {}
        #Loop over all rows of data table
        for i in range(len(self.data)):
            #For each row, makes the gene name the dictionary key, and the numpy array of expression data the associated value
            self.geneDict[self.data[i,0]] = self.data[i,1:].astype('float64')
        
        np.random.shuffle(pairs)
        sub = pairs[0:subset]
        correlations = []
        for genePair in sub:
            if(genePair[0] in self.geneDict and genePair[1] in self.geneDict):
                correlations.append(np.arctanh(np.corrcoef(self.geneDict[genePair[0]],self.geneDict[genePair[1]])[1,0]))
            else: 
                correlations.append(np.arctanh(0.0))
        corrArray = np.array(correlations)
        self.mean = np.mean(corrArray)
        self.std = np.std(corrArray)
        print(f'Subset {subset} std: {self.std}')
        print(f'Subset {subset} mean: {self.mean}')

        

        