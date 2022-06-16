from scipy import stats
import glob
import pandas as pd
import numpy as np

def calcHeatMap(folder,totalPos,totalNeg,outputName,numDatasets,numFolds):
    #Read in all files from a specified folder
    files = [file for file in glob.glob(f'{folder}/*')]
    #For each data file, create a numpy array, then add it to the dataset list
    datasets = []
    for fileName in files:
        dataFrame = pd.read_csv(fileName).to_numpy()
        datasets.append(dataFrame)

    #Create list of sets of positive genes and negative genes for each fold 
    posSets = []
    negSets = []
    for data in datasets:
        print(data)
        #Create empty sets for positive and negative genes to be added to
        posGenes = set()
        negGenes = set()
        #For all genes in the the dataset
        for i in range(len(data)):
            #If the gene is positive, i.e, the gene has 1 in the +/- column, add the gene name to the positive gene set
            if(data[i,2] == 1.0):
                posGenes.add(data[i,1])
            #Otherwise, add that gene name to the negative gene set
            else:
                negGenes.add(data[i,1])
        #Append each set to the respective set list
        posSets.append(posGenes)
        negSets.append(negGenes)

    #Intializie empty arrays of zeros to be filled in with calculated p values
    posDataTable = np.zeros((len(datasets),len(datasets)))
    negDataTable = np.zeros((len(datasets),len(datasets)))
    #Loop over all datasets
    for i in range(numDatasets):
        #Loop over all datasets again so every dataset is copared with one another
        for j in range(numFolds):
            #Calculate the p value for the overlap in genes for both positive and negative genes of two datasets
            posDataTable[i,j] = 1 - stats.hypergeom.cdf(len(posSets[i] & posSets[j]),totalPos,len(posSets[i]),len(posSets[j]))
            negDataTable[i,j] = 1 - stats.hypergeom.cdf(len(negSets[i] & negSets[j]),totalNeg,len(negSets[i]),len(negSets[j]))
    
    #Generate list of labels that will be uesd for both columns and rows, this process is currently hardcoded
    labels = []
    for i in range(10):
        for j in range(4):
            labels.append(f'Run {i+1}, Fold {j+1}')

    #Create dataframes from 
    posDataFrame = pd.DataFrame(posDataTable, columns=labels,index=labels)
    negDataFrame = pd.DataFrame(negDataTable,columns=labels,index=labels)
    posDataFrame.to_csv(f'./Yeast Resources/Heatmap Data/{outputName}_Pos.csv')
    negDataFrame.to_csv(f'./Yeast Resources/Heatmap Data/{outputName}_Neg.csv')

    
    

    
totalPosGenes = 100
totalNegGenes = 5958
calcHeatMap('./Yeast Resources/June-9-Reruns/Primig',totalPosGenes,totalNegGenes,'Test',10,4)
calcHeatMap('./Yeast Resources/June-9-Reruns/Brem24',totalPosGenes,totalNegGenes,'Brem24',10,4)
# x = {1,2,3}
# y = {1,2,3}
# print(len(x.intersection(y)))