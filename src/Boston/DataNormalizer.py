import pandas as pd
import math

#Read in data with pandas, get names of the columns, then convert DataFrame to numpy array
bostonData = pd.read_csv('./resources/Boston.csv')
labels = bostonData.columns
bostonDataArray = bostonData.to_numpy()

#Normalize Data
for i in range(len(bostonDataArray[0])):
    mean = bostonDataArray[:,i].sum() / len(bostonDataArray[:i])
    for j in range(len(bostonDataArray)):
        bostonDataArray[j,i] = math.log2(bostonDataArray[j,i]/mean)

normalizedData = pd.DataFrame(bostonDataArray,columns=labels)
normalizedData.to_csv('./resources/Boston.norm.csv',index=False)



