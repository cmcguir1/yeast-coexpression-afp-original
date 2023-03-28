import pandas as pd
import numpy as np
import glob

folder = './Yeast Resources/Pairwise/Spell/AllGO_Original_Struct/Original_113x25000x92_Test_(Old)/**'
files = [pd.read_csv(file).to_numpy() for file in glob.glob(folder) if 'GOTermDistribution' in file]

termIndices = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
termDict = {term[0]: term[1] for term in termIndices}

AUC_List = []
for term, index in termDict.items():
    termAUC = 0
    termPrec = 0
    for frame in files:
        termAUC += frame[termDict[term],1]
        termPrec += frame[termDict[term],2]
    termAUC /= 4
    termPrec /= 4
    AUC_List.append([term,termAUC,termPrec])
pd.DataFrame(AUC_List,columns=['Term','Avg AUC','Avg Prec']).to_csv('./AllGOTermAUC&AvgPrec.csv',index=False)
