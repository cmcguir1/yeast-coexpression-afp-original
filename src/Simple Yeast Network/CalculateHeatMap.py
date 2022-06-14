from scipy import stats
import glob
import pandas as pd
import numpy as np

def calcHeatMap(folder,totalPos,totalNeg,outputName):
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
    
    posDataTable = np.zeros((len(datasets),len(datasets)))
    negDataTable = np.zeros((len(datasets),len(datasets)))
    for i in range(len(datasets)):
        for j in range(len(datasets)):
            posDataTable[i,j] = 1 - stats.hypergeom.cdf(len(posSets[i] & posSets[j]),totalPos,len(posSets[i]),len(posSets[j]))
            negDataTable[i,j] = 1 - stats.hypergeom.cdf(len(negSets[i] & negSets[j]),totalNeg,len(negSets[i]),len(negSets[j]))
    
    labels = []
    for i in range(10):
        for j in range(4):
            labels.append(f'Run {i+1}, Fold {j+1}')
    #labels = ['1','2','3']

    posDataFrame = pd.DataFrame(posDataTable, columns=labels,index=labels)
    negDataFrame = pd.DataFrame(negDataTable,columns=labels,index=labels)
    posDataFrame.to_csv(f'./Yeast Resources/Heatmap Data/{outputName}_Pos.csv')
    negDataFrame.to_csv(f'./Yeast Resources/Heatmap Data/{outputName}_Neg.csv')

    
    

    
totalPosGenes = 100
totalNegGenes = 5958
calcHeatMap('./Yeast Resources/June-9-Reruns/Primig',totalPosGenes,totalNegGenes,'Test')
calcHeatMap('./Yeast Resources/June-9-Reruns/Brem24',totalPosGenes,totalNegGenes,'Brem24')
# x = {1,2,3}
# y = {1,2,3}
# print(len(x.intersection(y)))