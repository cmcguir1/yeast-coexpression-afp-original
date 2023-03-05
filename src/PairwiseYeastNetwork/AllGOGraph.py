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
    def __init__(self,networkPath,structure,folder,numfolds=4,geneFolds='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='modern',softmax=False):
        #Intialize file path for folder where results will be saved
        self.path = f'./Yeast Resources/GraphResults/{folder}'
        if(not os.path.exists(self.path)):
            os.mkdir(self.path)

        GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
        self.GOTermDict = {term[0]: term[1] for term in GoTerms}

        #Correlations Dictionary that will be retrieve precalculated correlation values
        self.corrDict = CorrelationDictionary(dictLoc='../YeastMemMap/YeastCorrDictionary.dat' if (os.path.exists('../YeastMemMap/YeastCorrDictionary.dat')) else '../YeastDict.dat',datasetType=ontologyDataset)
        self.datasets = self.corrDict.expDataset.datasets

        self.regularize = True
        self.leaves = getLeaves(10,dataset=ontologyDataset)

        #Intiailize list of networks and device tensor will be calculated on
        self.numFolds = numfolds
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.nets = []
        for i in range(numfolds):
            net = FlexNet(structure,sigmoid=False)
            net.load_state_dict(torch.load(f'{networkPath}{i+1}.pth'))
            net.to(self.device)
            self.nets.append(net)

        self.softmax = softmax
        self.sm = torch.nn.Softmax(dim=1)

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
                if self.softmax:
                    outputs = self.sm(outputs)
                
                labels = np.array(labels,dtype=np.intc)
                # print('------------------------------')
                # print(f'Gene A in : {pair[0] in posGenes}')
                # print(f'Gene B in : {pair[1] in posGenes}')
                # print(f'Desired GO Term: {outputs[0,self.GOTermDict[term]].item()}')
                # print(f'Other terms Labels:\n{labels}')
                # print(f'Other terms Scores:\n{outputs}')
                return [pair[0],pair[1],outputs[0,self.GOTermDict[term]].item()]

            
            
            #Set of all genes that are annotated to tested term
            if os.path.exists(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv'):
                posGenes = pd.read_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv').to_numpy().flatten()
            else:
                posGenes = getGenes(term,dataset=dataset)
                pd.DataFrame(posGenes,columns=['Gene']).to_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv',index=False)

            posSet = set(posGenes)
            
            foldPosGenes = [gene for gene in posGenes if gene in self.folds[fold]]
            agnGenes = pd.read_csv('./Yeast Resources/TermPos/AgnosticGenes.csv').to_numpy().flatten()
            

            
            pairs = AllGoGraph.makePairs(self.folds[fold],self.allGenes)

            #agnPairs = AllGoGraph.makePairs(self.folds[fold],agnGenes)
            agnPairs = AllGoGraph.makePairs(agnGenes,posGenes)

            if trackTime:
                foldScores = []
                start = time.time()
                for i,pair in enumerate(pairs,1):
                    foldScores.append(calcPair(pair))
                    #print(foldScores[i-1])
                    if i % 10000 == 0:
                        ratio = i/(len(pairs)+len(agnPairs))
                        print(f'Calculated {ratio*100}% of pairs\nEstimated Time Remaining: {((time.time()-start)/60) * (((len(pairs)+len(agnPairs)) - i) / i)}')
                
                agnScores = []
                for i,pair in enumerate(agnPairs,len(pairs)):
                    agnScores.append(calcPair(pair))
                    #print(agnScores[i-len(pairs)])
                    if i % 10000 == 0:
                        ratio = i/(len(pairs)+len(agnPairs))
                        print(f'Calculated {ratio*100}% of pairs\nEstimated Time Remaining: {((time.time()-start)/60) * (((len(pairs)+len(agnPairs)) - i) / i)}')
            else:
                foldScores = [calcPair(pair) for pair in pairs]
                agnScores = [calcPair(pair) for pair in agnPairs]

            pd.DataFrame(foldScores,columns=['Gene A', 'Gene B', 'Score']).to_csv(f'{self.path}/posScores_fold{fold}.csv',index=False)
            pd.DataFrame(agnScores,columns=['Gene A', 'Gene B', 'Score']).to_csv(f'{self.path}/agnScores_fold{fold}.csv',index=False)


    #rankGenes takes all of the calculated pair scores then ranks the genes by their involvment in a given process
    def rankGenes(self,term='GO:0007005',dataset='original',checkProportion=True):
        
        posGenes = getGenes(term,dataset=dataset)
        # negGenes = {gene for gene in [leaf for leaf in leaves if term[0] != term]}
        leaves = getLeaves(10,dataset=dataset)
        negTerms = [leaf[1] for leaf in leaves if leaf[0] != term]
        negGenes = set()
        for termGenes in negTerms:
            negGenes = negGenes | termGenes

        def checkPosNeg(gene):
            if gene in posGenes: 
                return 1
            elif gene in negGenes:
                return -1
            else:
                return 0
        
        posSet = set(posGenes)
        folds = [pd.read_csv(f'{self.path}/posScores_fold{i}.csv').to_numpy(dtype=object) for i in range(self.numFolds)]
        genePairs = np.concatenate(folds,axis=0)
        agnFolds = [pd.read_csv(f'{self.path}/agnScores_fold{i}.csv').to_numpy(dtype=object) for i in range(self.numFolds)]
        agnGenePairs = np.concatenate(agnFolds,axis=0)
        agnGenes = pd.read_csv('./Yeast Resources/TermPos/AgnosticGenes.csv').to_numpy().flatten()
        
        posScore = {}
        totalScore = {}

        for gene in self.allGenes:
            posScore[gene] = 0
            totalScore[gene] = 0
        for gene in agnGenes:
            posScore[gene] = 0
            totalScore[gene] = 0

        for genePair in genePairs:
            totalScore[genePair[0]] = totalScore[genePair[0]] + float(genePair[2])
            if genePair[1] in posSet:
                posScore[genePair[0]] = posScore[genePair[0]] + float(genePair[2])
        for genePair in agnGenePairs:
            totalScore[genePair[0]] = totalScore[genePair[0]] + (float(genePair[2]) / self.numFolds)
            if genePair[1] in posSet:
                posScore[genePair[0]] = posScore[genePair[0]] + (float(genePair[2]) / self.numFolds)
        
            
        if checkProportion:
            [[gene,checkPosNeg(gene),score/totalScore[gene]] for gene,score in posScore.items()]
        else:
            scoreTable = [[gene,checkPosNeg(gene),score] for gene,score in posScore.items()]
        confMat = ConfusionMatrix.calculateMatrix(np.array(scoreTable,dtype=object),1,2)
        pd.DataFrame(confMat,columns=['Gene','Label','Score','Precision','Recall','False Positive Rate']).to_csv(f'{self.path}/GeneRanking.csv',index=False)

    
    #Makes all possible pairs between 2 sets of genes
    def makePairs(set1,set2):
        pairs = []
        for gene1 in set1:
            for gene2 in set2:
                if gene1 != gene2:
                    pairs.append([gene1,gene2])
        return pairs
