import numpy as np
import pandas as pd
import sys
import time
import os

from ConfusionMatrix import ConfusionMatrix

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

class MemMapGraph():
    def __init__(self,scorePath,folder,pairsPath='./AllPairs.dat') -> None:
        # Memmap that holds the scores of each pair
        self.memMap = np.memmap(scorePath,dtype='float32',shape=(27830900+5850565,92),mode='r+')
        # Memmap that holds the names of each gene in each pair
        self.pairs = np.memmap(pairsPath,shape=(27830900+5850565,2),dtype='U10',mode='r+')

        # Initialize GO term index dictionary and array of all yeast genes
        GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
        self.GOTermDict = {term[0]: term[1] for term in GoTerms}
        self.allGenes = pd.read_csv('./src/PairwiseYeastNetwork/AllGOGeneFold1.csv').to_numpy()[:,0]
        

        self.folder = folder

    def rankTerm(self,term,saveLoc='./Yeast Resources/GraphResults/'):
        # Save index of particular term in scores memMap
        termIndex = self.GOTermDict[term]

        # Generate the set of positive and negative genes for this term
        # posGenes = set(getGenes(term))
        # leaves = getLeaves(10)
        # negGenes = set()
        # for leaf in leaves:
        #     if leaf[0] != term:
        #         negGenes = negGenes.union(leaf[1])
        # negGenes = negGenes - posGenes

        posGenes = pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Pos_original.txt').to_numpy().flatten()
        negGenes = pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Neg_original.txt').to_numpy().flatten()
        agnGenes = pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Agn_original.txt').to_numpy().flatten()
        genes = np.concatenate([posGenes,negGenes,agnGenes],0)

        # Initialize score dictionaries that will compute the total scores for each single gene
        posScore = {}
        totalScore = {}
        for gene in genes:
            posScore[gene] = 0
            totalScore[gene] = 0
        for gene in posGenes:
            posScore[gene] = 0
            totalScore[gene] = 0
        for gene in negGenes:
            posScore[gene] = 0
            totalScore[gene] = 0

        # Loop over all pairs in the memMap
        pairLen = len(self.pairs)
        increment = pairLen / 10000
        start = time.time()
        print('Start Calculations')
        for i in range(pairLen):
            
            if not(self.pairs[i,0] in posScore or self.pairs[i,0 in totalScore]):
                posScore[self.pairs[i,0]] = 0
                totalScore[self.pairs[i,0]] = 0
            # If Gene A is paired with a positive Gene B, add that confidence score to the total
            if self.pairs[i,1] in posGenes:
                posScore[self.pairs[i,0]] = posScore[self.pairs[i,0]] + self.memMap[i,termIndex]
            # Also keep track of the score of a gene's connection to every other gene
            totalScore[self.pairs[i,0]] = totalScore[self.pairs[i,0]] + self.memMap[i,termIndex]
            if i % 10000 == 0 and i != 0:
                print(f'Calculated {(i/pairLen)*100}% of the pairs\nTime elapsed: {(time.time() - start) / 60}')
        
        singleGenes = []
        for gene, score in posScore.items():
            
            if gene in posGenes:
                label = 1
            elif gene in negGenes:
                label = -1
            else:
                label = 0
            if score != 0:
                singleGenes.append([gene,label,score,totalScore[gene]])

        print(singleGenes)
        cm = ConfusionMatrix.calculateMatrix(singleGenes,1,2)
        if not os.path.exists(f'{saveLoc}{self.folder}'):
            os.makedirs(f'{saveLoc}{self.folder}')
        pd.DataFrame(cm,columns=['Gene','Label','Score','Background Score','Precision','Recall','False Positive Rate']).to_csv(f'{saveLoc}{self.folder}/{term.replace(":","-")}_GeneRanking.csv',index=False)
        


        

        


