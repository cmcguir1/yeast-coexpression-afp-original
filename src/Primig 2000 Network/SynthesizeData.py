import math
import pandas as pd
import numpy as np
from YeastData import YeastData

#Read in template file, then save its column names
template = pd.read_csv("./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl",sep='\t')
columnNames = list(template)

#Convert DataFrame into an array
templateArray = template.to_numpy()

#Variables for the signal strength and noise of the data
signal = 2
noise = 1

#Loop over all rows of data table
for i in range(len(templateArray)):
    #If gene in row is positive, then introduce a signal with some noise to each item in the row
    if(templateArray[i,0] in YeastData.posSet):
        for j in range(len(templateArray[i])-3):
            templateArray[i,j+3] = signal * math.sin((2/24)*2*math.pi) + noise * np.random.normal()
    #If gene is negative, make each item in row noise
    else:
        for j in range(len(templateArray[i])-3):
            templateArray[i,j+3] = np.random.normal()

#Convert templateArray into dataFrame, then save file to specified location
syntheticData = pd.DataFrame(templateArray,columns=columnNames)
syntheticData.to_csv('./Yeast Resources/Synthetic_NegativeControl.csv',index=False)
