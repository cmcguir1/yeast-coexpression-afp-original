import pandas as pd
import numpy as np

SingleTerm = pd.read_csv('./src/PairwiseYeastNetwork/Compare/SingleTermAUC&AvgPrec.csv').to_numpy()
AllGO = pd.read_csv('./src/PairwiseYeastNetwork/Compare/AllGOTermAUC&AvgPrec.csv').to_numpy()
data = [[SingleTerm[i,0],SingleTerm[i,1],SingleTerm[i,2],AllGO[i,1],AllGO[i,2],AllGO[i,1]-SingleTerm[i,1],AllGO[i,2]-SingleTerm[i,2]] for i in range(len(SingleTerm))]
pd.DataFrame(data,columns=['Term','Single AUC','Single Avg Prec','AllGO AUC','AllGO Avg Prec','AUC Diff','Avg Prec Diff']).to_csv('./src/PairwiseYeastNetwork/Compare/TermAUC_Differnces.csv',index=False)