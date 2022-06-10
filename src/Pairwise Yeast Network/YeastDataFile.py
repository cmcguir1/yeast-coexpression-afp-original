from cProfile import label
import pandas as pd

#Takes a filePath, then creates a gene dictionary
class YeastDataFile():
    def __init__(self,filePath):
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

        