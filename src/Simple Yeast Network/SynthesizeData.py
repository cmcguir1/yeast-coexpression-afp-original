import math
import pandas as pd
import numpy as np
from YeastData import YeastData

#Read in template file, then save its column names
def synthesize(totalPos,totalNeg,fileName,templateFile="./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl"):
    template = pd.read_csv(templateFile,sep='\t')
    columnNames = list(template)

    #Convert DataFrame into an array
    templateArray = template.to_numpy()

    #Variables for the signal strength and noise of the data
    signal = 0.25
    noise = 1
    pos = 0
    neg = 0

    templateList = []
    #Loop over all rows of data table
    for i in range(len(templateArray)):
        #If gene in row is positive, then introduce a signal with some noise to each item in the row
        if(templateArray[i,0] in YeastData.posSet and pos < totalPos):
            for j in range(len(templateArray[i])-3):
                templateArray[i,j+3] = signal * math.sin((j/24)*2*math.pi) + noise * np.random.normal()
            templateList.append(templateArray[i])
            pos += 1

        #If gene is negative, make each item in row noise
        elif(not(templateArray[i,0] in YeastData.posSet) and neg < totalNeg):
            for j in range(len(templateArray[i])-3):
                templateArray[i,j+3] = np.random.normal()
            templateList.append(templateArray[i])
            neg += 1
    syntheticArray = np.array(templateList)

    #Convert templateArray into dataFrame, then save file to specified location
    syntheticData = pd.DataFrame(syntheticArray,columns=columnNames)
    syntheticData.to_csv(fileName,sep='\t',index=False)

for i in range(5):
    synthesize(36,264,f'./Yeast Resources/Datasets/Synthetic/Small 36-264/Small_36-264_{i+1}.txt')
