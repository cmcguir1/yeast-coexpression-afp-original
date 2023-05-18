from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import time
import os

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
GOTermDict = {term[0]: term[1] for term in GoTerms}

bioProc = getGenes('GO:0008150')
print((bioProc))
#pd.DataFrame(bioProc,columns=['Genes']).to_csv('./Yeast Resources/GeneSets/BiologicalProcessGenes.csv',index=False)
print(len(pd.read_csv('./Yeast Resources/GeneSets/BiologicalProcessGenes.csv').values.flatten().tolist()))

# for term, value in GOTermDict.items():
#     if (os.path.exists(f"./Yeast Resources/GraphResults/AllSingle_New/{term.replace(':','')}_PosPairs_Fold1.csv") and
#         os.path.exists(f"./Yeast Resources/GraphResults/AllSingle_New/{term.replace(':','')}_PosPairs_Fold2.csv") and
#         os.path.exists(f"./Yeast Resources/GraphResults/AllSingle_New/{term.replace(':','')}_PosPairs_Fold3.csv") and
#         os.path.exists(f"./Yeast Resources/GraphResults/AllSingle_New/{term.replace(':','')}_PosPairs_Fold4.csv")):
#         start = time.time()
#         posGenes = set(pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Pos_original.txt').to_numpy().flatten())
#         negGenes = set(pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Neg_original.txt').to_numpy().flatten())
#         agnGenes = set(pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Agn_original.txt').to_numpy().flatten())
        
#         data = [pd.read_csv(f"./Yeast Resources/GraphResults/AllSingle_New/{term.replace(':','')}_PosPairs_Fold{i}.csv").to_numpy() for i in range(1,5)]
#         arr = np.concatenate(data,0)
#         newData= []
#         for row in arr:
#             if row[0] in posGenes and row[1] in posGenes:
#                 newData.append([row[0],row[1],row[2],1])
#             else:
#                 newData.append([row[0],row[1],row[2],-1])
#         pd.DataFrame(newData,columns=['Gene A','Gene B','Score','Label']).to_csv(f"./Yeast Resources/GraphResults/AllSingle_New/{term.replace(':','')}_PosPairs_Combined.csv",index=False)
#         print(f'Time to calculate: {(time.time()-start)/60} minutes')
