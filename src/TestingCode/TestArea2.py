import pandas as pd
import numpy as np

local = pd.read_csv('./Yeast Resources/Datasets/All Spell/YeastLocalizationData.txt',sep="\t",index_col=False).drop(['Unnamed: 32'],axis=1)
cols = local.columns
local = local.to_numpy()
localizationMap = {}
for row in local:
    localizationMap[row[1]] = row[9:]
print(localizationMap)
print(cols[9:])

