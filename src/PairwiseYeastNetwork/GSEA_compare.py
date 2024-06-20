import pandas as pd
import numpy as np

import sys
sys.path.insert(0,'./obopy')
from GOParser import GOParser

parser = GOParser('2023')

def compare(filename1,model1,filename2,model2):
    

    df1 = pd.read_csv(filename1)
    df2 = pd.read_csv(filename2)


    dict1 = {}
    dict2 = {}
    for index, row in df1.iterrows():
        dict1[row['GO Term ID']] = (row['NES'],row['FDR q-value'])

    for index, row in df2.iterrows():
        dict2[row['GO Term ID']] = (row['NES'],row['FDR q-value'])

    table =[]
    for term, (nes_1,q_1) in dict1.items():
        numGenes = len(parser.getGenes(term))
        if term in dict2:
            nes_2, q_2 = dict2[term]
            if q_1 <= 0.05 or q_2 <= 0.05:
                table.append([term,parser.onto.terms[term].name,numGenes,nes_1,q_1,nes_2,q_2,nes_1-nes_2])

    pd.DataFrame(table,columns=['GO Term ID','GO Term Name','Num GO Term Annos',f'{model1} Nes',f'{model1} q-value',f'{model2} NES',f'{model2} q-value','NES Difference']).to_csv(f'./Yeast Resources/GSEA_redo/Comparisons/GSEA_{model1}_{model2}_Comparison.csv',index=False)

filename1 = './Yeast Resources/GSEA_redo/GSEA_redoGSEA_NN_-_-.csv'
filename2 = './Yeast Resources/GSEA_redo/GSEA_redoGSEA_SPELL_-_-.csv'

model1 = 'NN_-_-'
model2 = 'SPELL_-_-'
compare(filename1,model1,filename2,model2)