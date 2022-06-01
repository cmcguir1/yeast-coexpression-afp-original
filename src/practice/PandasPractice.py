import pandas as pd
import numpy as np
import torch

dataArray = pd.read_csv('./resources/IRIS.csv').to_numpy()
setosaArray = dataArray[0:50].copy()
versicolorArray = dataArray[50:100].copy()
viginicaArray = dataArray[100:150].copy()

print(setosaArray)
#print(versicolorArray)
#print(viginicaArray)

np.random.shuffle(setosaArray)
np.random.shuffle(versicolorArray)
np.random.shuffle(viginicaArray)

print(dataArray)
print(setosaArray)
#print(versicolorArray)
#print(viginicaArray)



