from scipy import stats
import numpy as np
import pandas as pd
import sys
sys.path.append('./obopy/')
from Leaf import getGenes

def calcOverlap(foldFile,numFolds,posFile,term):
    #Read in genes from fold file
    data = pd.read_csv(foldFile).to_numpy()
    #Read in set of positive gnees
    posGenes = set(pd.read_csv(posFile).to_numpy().flatten())
    #Make an empty set for each fold
    folds = []
    for i in range(numFolds):
        folds.append(set())
    #For every gene in the fold file, add that gene
    for row in data:
        if(row[1] == 1):
            folds[int(row[2])].add(row[0])
    mitoGenes = set(getGenes(term))
    foldNum = 1
    for fold in folds:
        print('')
        print(f"Fold {foldNum}")
        foldNum += 1
        print(f'Overlap: {len(set(mitoGenes) & fold)}')
        print(f'Total Positives: {len(posGenes)}')
        print(f'Genes in Fold: {len(fold)}')
        print(f'Positive Mitochandria Genes: {len(posGenes & mitoGenes)}')
        pvalue = 1 - stats.hypergeom.cdf(len(set(mitoGenes) & fold),len(posGenes),len(fold),len(posGenes & mitoGenes))
        print(f'p-value: {pvalue}')

goTerms = ['GO:0010823','GO:0097250','GO:0008053','GO:0048311','GO:0140655','GO:0006626','GO:0008637','GO:0010821','GO:0030382','GO:0070584','GO:0007006','GO:0033108','GO:0000002','GO:0010822','GO:0000266','GO:0061726']
for term in goTerms:
    print(f'Term: {term}')
    calcOverlap('./Yeast Resources/Datasets/All Spell/GeneFolds1.csv',4,'./Yeast Resources/positives_00_go04-15-07.txt',term)
    print('-------------------------------------------------------------------')
    
    