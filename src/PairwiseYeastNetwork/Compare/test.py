import numpy as np
import pandas as pd

allGenes = pd.read_csv('./src/PairwiseYeastNetwork/AllGOGeneFold1.csv').to_numpy()[:,0]
print(allGenes)