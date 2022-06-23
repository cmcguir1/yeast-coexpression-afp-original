from operator import index
import numpy as np
import pandas as pd

ensembleDataFrame = pd.read_csv('./Yeast Resources/ensembleData.csv',index_col=False)
names = ensembleDataFrame.columns.values
cols = columns=[*names[0:5],*['Positive','Negative','Agnostic'],*names[5:]]
ensembleData = ensembleDataFrame.to_numpy()
ensemble = np.concatenate((ensembleData[:,0:5],np.zeros((len(ensembleData),3)),ensembleData[:,5:]),1)
positives = set(pd.read_csv('./Yeast Resources/positives_00_go04-15-07.txt').to_numpy().flatten())
negatives = set(pd.read_csv('./Yeast Resources/negatives_00_go04-15-07.txt').to_numpy().flatten())
agnostics = set(pd.read_csv('./Yeast Resources/agnostic_01_underannotated.txt').to_numpy().flatten())

dataTable = []
for data in ensemble:
    if(data[0] in positives):
        data[5] = 1
    elif(data[0] in negatives):
        data[6] = 1
    elif(data[0] in agnostics):
        data[7] = 1

dataFrame = pd.DataFrame(ensemble,columns=cols)
dataFrame.to_csv('./Yeast Resources/ensembleData_membership.csv',index=False)
