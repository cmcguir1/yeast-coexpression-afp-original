from cProfile import label
import pandas as pd
import numpy as np
import time

#Takes a filePath, then creates a gene dictionary
class YeastDataFile():
    def __init__(self,filePath,pairs,subset):
        #Reads in file from filePath, expected to be tab delimited, then drops the NAME and GWEIGHT columns can converts to numpy
        print(filePath)
        self.data = pd.read_csv(filePath,sep='\t').to_numpy()       #.drop(labels=['NAME','GWEIGHT'],axis=1).to_numpy()
        self.data = np.delete(self.data,1,1)
        self.data = np.delete(self.data,1,1)
        

        #Removes first row from data array as it will always be the number 1
        self.data = self.data[1:]

        #dataFile stores the name of the data file, including which folder the file is found within Yeast Resources
        self.dataFile = filePath[filePath.find('\\')+1:]

        #Intializes an empty gene dictionary that will take in a gene in return its expression data for this dataset
        self.geneDict = {}
        #Loop over all rows of data table
        for i in range(len(self.data)):
            #For each row, makes the gene name the dictionary key, and the numpy array of expression data the associated value
            self.geneDict[self.data[i,0]] = self.data[i,1:].astype('float64')
        
        #Shuffle order of pairs array so that we are randomly sampling when we calculate mean and std
        np.random.shuffle(pairs)
        #Take first subset gene pairs as sample
        sub = pairs[0:subset]
        #Intialize empty correlations list
        correlations = []
        #Loop over all pairs in subset
        for genePair in sub:
            correlations.append(np.arctanh(self.customCorrelation(genePair=genePair)))

            # #If gene pair is in this dataset's gene dictionary, calculate the fisher z transform of the pearson correlation between the genes
            # #The second half of the compounded boolean checks that both gene pair arrays do not contain nan values
            # if(genePair[0] in self.geneDict and genePair[1] in self.geneDict and self.validGeneData(genePair=genePair)):      # and (len(self.geneDict[genePair[0]]) == len(self.geneDict[genePair[1]]))
            #     # print(f'Gene A: {self.geneDict[genePair[0]]}')
            #     # print(f'Gene B: {self.geneDict[genePair[1]]}')
            #     correlations.append(np.arctanh(np.corrcoef(self.geneDict[genePair[0]],self.geneDict[genePair[1]])[1,0]))
            # #If the gene pair is not in the gene dictionary, assume that the pearson correlation is 0
            # else: 
            #     correlations.append(np.arctanh(0.0))

        #Convert list to numpy array, then used numpym methods to calculate mean and standard deviation
        corrArray = np.array(correlations)
        #nanmean and nanstd ingnores nan values
        self.mean = np.mean(corrArray)
        self.std = np.std(corrArray)
        # print(f'File: {self.dataFile}')
        # print(f'Numpy array:')
        # print(self.data)
        print(f'Subset {subset} std: {self.std}')
        print(f'Subset {subset} mean: {self.mean}')

    def customCorrelation(self,genePair):
        #First checks if the gene pair is in this dataset's gene library
        if(genePair[0] in self.geneDict and genePair[1] in self.geneDict):
            geneA = self.geneDict[genePair[0]]
            geneB = self.geneDict[genePair[1]]
            validIndicies = []
            #Loop over all elements of geneA and geneB, and append the index of each element to a list if both elements are valid
            for i in range(len(geneA)):
                if not(geneA[i] == np.nan or geneA[i] == 1.0 or geneA[i] == 0.0 or geneB[i] == np.nan or geneB[i] == 1.0 or geneB[i] == 0.0):
                    validIndicies.append(i)
            #If there are half or less valid indicies, return 0
            if len(validIndicies) <= float(len(geneA)) / 2.0:
                return 0.0
            #Otherwise, construct filtered arrays for gene A and B, then return their pearson correlation
            else:
                geneAList = []
                geneBList = []
                for index in validIndicies:
                    geneAList.append(geneA[index])
                    geneBList.append(geneB[index])
                geneAFilter = np.array(geneAList)
                geneBFilter = np.array(geneBList)
                if(np.corrcoef(geneAFilter,geneBFilter)[1,0] == np.nan):
                    print(f'Gene List A: {geneAList}')
                    print(f'Gene List B: {geneBList}')
                    print(f'Gene Array A: {geneAFilter}')
                    print(f'Gene Array B: {geneBFilter}')
                    print(f'Corr Coeff: {np.corrcoef(geneAFilter,geneBFilter)[1,0]}')
                return np.corrcoef(geneAFilter,geneBFilter)[1,0]
        #If gene pair is not in this dataset's dictionary, return 0, i. e. there is no correlation between these genes
        else:
            return 0.0

        

        