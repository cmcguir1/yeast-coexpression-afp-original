from __future__ import generator_stop
import sys
import pandas as pd

sys.path.insert(0,'./obopy')
import Leaf

# slim = open('C:/Users/colem/SummerResearch2022/obopy/goslim_yeast.obo')
# lines = slim.readlines()
# termDict = []
# for i in range(len(lines)):
#     if '[Term]' in lines[i] :
#         term = lines[i+1][4:-1]
#         name = lines[i+2][6:-1]
#         print(term)
#         print(name)
#         termDict.append([term,name])
# pd.DataFrame(termDict,columns=['Term','Term Name']).to_csv('./src/PairwiseYeastNetwork/TermNameDict.csv',index=False)

termArray = pd.read_csv('./src/PairwiseYeastNetwork/TermNameDict.csv').to_numpy()
termDict = {}
for term in termArray:
    termDict[term[0]] = term[1]

