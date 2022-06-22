import pandas as pd
import numpy as np

data = pd.read_csv('./Yeast Resources/ensembleData.csv',index_col=False)
names = data.columns
data = data.to_numpy()
print(data)
print(names)
dataTable = []

def confusionMatrix(dataArray):
    
    pos = 0
    neg = 0
    for row in dataTable:
        if(row[4] == 1):
            pos += 1
        elif(row[2] == 0):
            neg += 1
    
    truePos = pos
    falsePos = neg
    trueNeg = 0
    falseNeg = 0

    dataTable = []
    for row in dataArray:
        if(row[4] == 1):
            truePos -= 1
            falseNeg += 1
            dataTable.append([row[0],truePos,falsePos,trueNeg,falseNeg])
        elif(row[2] == 0):
            falsePos -= 1
            trueNeg += 1
            dataTable.append([row[0],truePos,falsePos,trueNeg,falseNeg])
            
    return np.array(dataTable)

