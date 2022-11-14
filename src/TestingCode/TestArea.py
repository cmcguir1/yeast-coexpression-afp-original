from __future__ import generator_stop
import sys
import pandas as pd

sys.path.insert(0,'./obopy')
import Leaf

data = pd.read_csv('./src/PairwiseYeastNetwork/datasetDictionary.csv').to_numpy()
newFile = []
for file in data:
    a = file[0]
    newFile.append([a[a.rfind('\\')+1:],file[1]])

print(newFile)
pd.DataFrame(newFile,columns=['Dataset','Index']).to_csv('./src/PairwiseYeastNetwork/datasetDictionaryRevised.csv',index=False)

print(newFile)
