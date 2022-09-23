from __future__ import generator_stop
import sys
import pandas as pd

sys.path.insert(0,'./obopy')
import Leaf

bioPro = set(Leaf.getGenes('GO:0008150'))
pos = set(pd.read_csv('./Yeast Resources/positives_00_go04-15-07.txt').to_numpy().flatten())
neg = set(pd.read_csv('./Yeast Resources/negatives_00_go04-15-07.txt').to_numpy().flatten())
agn = set(pd.read_csv('./Yeast Resources/agnostic_01_underannotated.txt').to_numpy().flatten())
allGenes = bioPro | pos | neg | agn
print(f'Length of all yeast genes: {len(allGenes)}')

geneDict = [[gene,index] for index, gene in enumerate(allGenes)]
pd.DataFrame(geneDict,columns=['Gene','Index']).to_csv('./src/PairwiseYeastNetwork/geneIndexDictionary_full.csv',index=False)