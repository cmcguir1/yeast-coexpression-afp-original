import pandas as pd
import numpy as np

import sys
sys.path.insert(0,'./obopy')
from GOParser import GOParser

parser = GOParser('2023')


filename1 = './Yeast Resources/GSEA/GSEA_NN.csv'
filename2 = './Yeast Resources/GSEA/GSEA_SPELL.csv'

df1 = pd.read_csv(filename1)
df2 = pd.read_csv(filename2)


dict1 = {}
dict2 = {}
for index, row in df1.iterrows():
    dict1[row['GO Term ID']] = row['NES']

for index, row in df2.iterrows():
    dict2[row['GO Term ID']] = row['NES']

table =[]
for term, nes in dict1.items():
    numGenes = len(parser.getGenes(term))
    table.append([term,parser.onto.terms[term].name,numGenes,nes,dict2[term],nes-dict2[term]])

pd.DataFrame(table,columns=['GO Term ID','GO Term Name','Num Genes','NN Nes','SPELL NES','NES Difference']).to_csv('./Yeast Resources/GSEA/GSEA_NN_SPELL_Comparison.csv',index=False)

