from scipy import stats
import numpy as np
import pandas as pd
import sys
sys.path.append('./obopy/')
from Leaf import getGenes

def calcOverlap(foldFile,numFolds,posFile,term):
    data = pd.read_csv(foldFile).to_numpy()
    posGenes = set(pd.read_csv(posFile).to_numpy().flatten())
    folds = []
    for i in range(numFolds):
        folds.append(set())
    for row in data:
        if(row[1] == 1):
            folds[int(row[2])].add(row[0])
    mitoGenes = set(getGenes(term))
    for fold in folds:
        print(f'Overlap: {len(set(mitoGenes) & fold)}')
        print(f'Total Positives: {len(posGenes)}')
        print(f'Genes in Fold: {len(fold)}')
        print(f'Positive Mitochandria Genes: {len(posGenes & mitoGenes)}')
        pvalue = 1 - stats.hypergeom.cdf(len(set(mitoGenes) & fold),len(posGenes),len(fold),len(posGenes & mitoGenes))
        print(f'p-value: {pvalue}')

calcOverlap('./Yeast Resources/Datasets/All Spell/GeneFolds1.csv',4,'./Yeast Resources/positives_00_go04-15-07.txt','GO:0005761')
    