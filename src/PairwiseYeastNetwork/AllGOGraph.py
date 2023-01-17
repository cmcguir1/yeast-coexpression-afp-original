import numpy as np
import pandas as pd
import torch
from AllGoModel import AllGoModel
import os
from FlexNet import FlexNet
from ConfusionMatrix import ConfusionMatrix
from CorrelationDictionary import CorrelationDictionary
import time

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

class AllGoGraph(AllGoModel):
    def __init__(self,networkPath,structure,folder,numfolds=4,geneFolds='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',memMapLoc='../YeastDict.dat'):
        #Intialize file path for folder where results will be saved
        self.path = f'./Yeast Resources/GraphResults/{folder}'
        if(not os.path.exists(self.path)):
            os.mkdir(self.path)

        GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
        self.GOTermDict = {term[0]: term[1] for term in GoTerms}

        #Correlations Dictionary that will be retrieve precalculated correlation values
        self.corrDict = CorrelationDictionary(dictLoc=memMapLoc,datasetType='modern')
        self.datasets = self.corrDict.expDataset.datasets

        self.regularize = True
        self.leaves = getLeaves(10,dataset='modern')

        #Intiailize list of networks and device tensor will be calculated on
        self.numFolds = numfolds
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.nets = []
        for i in range(numfolds):
            net = FlexNet(structure)
            net.load_state_dict(torch.load(f'{networkPath}{i+1}.pth'))
            net.to(self.device)
            self.nets.append(net)

        #Reads in folds file, then divides the folds up into sets of genes
        foldTable = pd.read_csv(geneFolds).to_numpy()
        self.folds = [{gene[0] for gene in foldTable if gene[1] == i} for i in range(numfolds)]
        self.allGenes = {gene[0] for gene in foldTable}


    def feedForward(self,fold,term='GO:0007005',trackTime=True,dataset='original'):
        with torch.no_grad():
            def calcPair(pair):
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device).float()
                outputs = self.nets[fold](features,test=True)
                
                labels = np.array(labels,dtype=np.intc)
                return [pair[0],pair[1],outputs[0,self.GOTermDict[term]]]

            
            
            #Set of all genes that are annotated to tested term
            if os.path.exists(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv'):
                posGenes = pd.read_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv').to_numpy().flatten()
            else:
                posGenes = getGenes(term,dataset=dataset)
                pd.DataFrame(posGenes,columns=['Gene']).to_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv',index=False)

            foldPosGenes = [gene for gene in posGenes if gene in self.folds[fold]]
            agnGenes = pd.read_csv('./Yeast Resources/TermPos/AgnosticGenes.csv')

            # leaves = getLeaves(10,dataset=dataset)
            # negTerms = [leaf[1] for leaf in leaves if term[0] != term]
            # negGenes = set()
            # for termGenes in negTerms:
            #     negGenes = negGenes | termGenes
            
            # #Set of all genes that are annoated to biological process, but are not annotated in the GO Slim
            # agnGenes = set(getGenes('GO:0008150',dataset=dataset)) - negGenes
            # pd.DataFrame(agnGenes,columns=['Gene']).to_csv('./Yeast Resources/TermPos/AgnosticGenes.csv',index=False)

            

            pairs = AllGoGraph.makePairs(self.folds[fold],posGenes)
            agnPairs = AllGoGraph.makePairs(self.folds[fold],agnGenes)

            if trackTime:
                foldScores = []
                start = time.time()
                for i,pair in enumerate(pairs,1):
                    foldScores.append(calcPair(pair))
                    if i % 10000 == 0:
                        ratio = i/(len(pairs)+len(agnPairs))
                        print(f'Calculated {ratio*100}% of pairs\nEstimated Time Remaining: {((time.time()-start)/60) * (((len(pairs)+len(agnPairs)) - i) / i)}')
                
                agnScores = []
                for i,pair in enumerate(agnPairs,len(pairs)):
                    agnScores.append(calcPair(pair))
                    if i % 10000 == 0:
                        ratio = i/(len(pairs)+len(agnPairs))
                        print(f'Calculated {ratio*100}% of pairs\nEstimated Time Remaining: {((time.time()-start)/60) * (((len(pairs)+len(agnPairs)) - i) / i)}')
            else:
                foldScores = [calcPair(pair) for pair in pairs]
                agnScores = [calcPair(pair) for pair in agnPairs]

            pd.DataFrame(foldScores,columns=['Gene A', 'Gene B', 'Score']).to_csv(f'{self.path}/posScores_fold{fold}.csv',index=False)
            pd.DataFrame(agnScores,columns=['Gene A', 'Gene B', 'Score']).to_csv(f'{self.path}/agnScores_fold{fold}.csv',index=False)

    #rankGenes takes all of the calculated pair scores then ranks the genes by their involvment in a given process
    def rankGenes(self,term='GO:0007005'):
        leaves = getLeaves(10)
        posGenes = leaves[leaves.index(term)][1]
        negGenes = {gene for gene in [leaf for leaf in leaves if term[0] != term]}
        agnGenes = set(getGenes('GO:0008150')) - negGenes
        def checkPosNeg(gene):
            if gene in posGenes:
                return 1
            elif gene in negGenes:
                return -1
            else:
                return 0
        
        
        folds = [pd.read_csv(f'{self.path}/posScores_fold{i}.csv').to_numpy() for i in range(self.numFolds)]
        genePairs = np.concatenate(folds,axis=1)
        agnFolds = [pd.read_csv(f'{self.path}/agnScores_fold{i}').to_numpy() for i in range(self.numFolds)]
        agnGenePairs = np.concatenate(agnFolds,axis=1)
        scoreDict = {}
        for genePair in genePairs:
            scoreDict[genePair[0]] = scoreDict[genePair[0]] + genePair[2]
        for genePair in agnGenePairs:
            scoreDict[genePair[0]] = scoreDict[genePair[0]] + (genePair[2] / self.numFolds)

        scoreTable = [[gene,checkPosNeg(gene),score] for gene,score in scoreDict.items()]
        confMat = ConfusionMatrix.calculateMatrix(scoreTable,1,2)
        pd.DataFrame(confMat,columns=['Gene','Label','Score','Precision','Recall','False Positive Rate']).to_csv(f'{self.path}/GeneRanking.csv')

    
    #Makes all possible pairs between 2 sets of genes
    def makePairs(set1,set2):
        pairs = []
        for gene1 in set1:
            for gene2 in set2:
                if gene1 != gene2:
                    pairs.append([gene1,gene2])
        return pairs
