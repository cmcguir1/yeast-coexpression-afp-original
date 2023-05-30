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
    def __init__(self,networkPath,structure,folder,numfolds=4,geneFolds='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='modern',calcDataset='original',softmax=False,inputVector='xl',outputVector='b',addTerms=[]):
        #Intialize file path for folder where results will be saved
        self.path = f'./Yeast Resources/GraphResults/{folder}'
        if(not os.path.exists(self.path)):
            os.mkdir(self.path)

        self.inputSize = 0

        # These four booleans are used for control flow later of data inclusion throughout the Model Object
        self.expression = 'x' in inputVector
        self.localization = 'l' in inputVector
        self.genomicInteraction = 'g' in inputVector
        self.physical = 'p' in inputVector

        if self.expression:
            # Correlations Dictionary that will be retrieve precalculated correlation values
            self.corrDict = CorrelationDictionary(dictLoc='../YeastMemMap/YeastCorrDictionary.dat' if (os.path.exists('../YeastMemMap/YeastCorrDictionary.dat')) else '../YeastDict.dat',datasetType=ontologyDataset,inMemory=False)
            self.datasets = self.corrDict.expDataset.datasets
            self.inputSize += len(self.datasets)
            print('Initialized Expression Datasets')

        if self.localization:
            # Localization Data Map
            localizationData = pd.read_csv('./Yeast Resources/Datasets/All Spell/YeastLocalizationData.txt',sep="\t",index_col=False).drop(['Unnamed: 32'],axis=1).to_numpy()
            self.localMap = {}
            for row in localizationData:
                self.localMap[row[1]] = [local == 'T' for local in row[9:]]
            self.inputSize += 23
            print('Initialized Localization Data')

        if self.genomicInteraction:
            # Dataset of all bioGRID interactions
            interactions = pd.read_csv('./InteractionData.txt',sep="\t").to_numpy()
            interactionsList = pd.read_csv('./bioGRID_Interactions.csv').to_numpy().flatten()
            # genomic index maps the genomic interactions we care about to an index
            genomicIndex = {item: i for i, item in enumerate(interactionsList[9:])}
            
            self.genomicMap = {}
            for row in interactions:
                # The string of the concatenated gene pair must be stored for both orders of which gene is first
                genePairStrA = row[0] + " " + row[1]
                genePairStrB = row[1] + " " + row[0]
                if (not (genePairStrA in self.genomicMap)) or (not (genePairStrB in self.genomicMap)):
                    self.genomicMap[genePairStrA] = [0 for i in range(6)]
                    self.genomicMap[genePairStrB] = [0 for i in range(6)]
                if row[6] in genomicIndex:
                    # If a gene pair has a interaction, change the value of the interactions list for that pair from 0 to 1 at that specific interaction's index
                    tmp = self.genomicMap[genePairStrA]
                    tmp[genomicIndex[row[6]]] = 1
                    self.genomicMap[genePairStrA] = tmp
                    self.genomicMap[genePairStrB] = tmp
            
            self.inputSize += 6
                

        if self.physical:
            # Dataset of all bioGRID interactions
            interactions = pd.read_csv('./InteractionData.txt',sep="\t").to_numpy()
            interactionsList = pd.read_csv('./bioGRID_Interactions.csv').to_numpy().flatten()
            
            # physical index maps physical interactions to indicies
            physicalIndex = {item: i for i, item in enumerate(interactionsList[2:9])}
            # All types of affinity capture are represented by one node, so they are all mapped to index 0
            physicalIndex['Affinity Capture-MS'] = 0
            physicalIndex['Affinity Capture-Western'] = 0
            
            
            self.physicalMap = {}
            for row in interactions:
                # The string of the concatenated gene pair must be stored for both orders of which gene is first
                genePairStrA = row[0] + " " + row[1]
                genePairStrB = row[1] + " " + row[0]
                if (not (genePairStrA in self.physicalMap)) or (not (genePairStrB in self.physicalMap)):
                    self.physicalMap[genePairStrA] = [0 for i in range(7)]
                    self.physicalMap[genePairStrB] = [0 for i in range(7)]
                if row[6] in physicalIndex:
                    # If a gene pair has a interaction, change the value of the interactions list for that pair from 0 to 1 at that specific interaction's index
                    tmp = self.physicalMap[genePairStrA]
                    tmp[physicalIndex[row[6]]] = 1
                    self.physicalMap[genePairStrA] = tmp
                    self.physicalMap[genePairStrB] = tmp
            
            self.inputSize += 7


        #   outputVector determines what types of GO terms are included as labels for the output vector
        #       b - Biological Processes
        #       m - Molecular Functions
        #       c - Cellular Components       
        #   Additional GO terms can be added with 'addTerm' """
        
        self.leaves = getLeaves(10,dataset=ontologyDataset,bioProc=('b' in outputVector),molFunc=('m' in outputVector),cellComp=('c' in outputVector))
        for term in addTerms:
            self.leaves.append([term,set(getGenes(term,dataset=ontologyDataset))])
        self.GOTermDict = {term[0]: i for i,term in enumerate(self.leaves)}



        self.regularize = True


        #Intiailize list of networks and device tensor will be calculated on
        self.numFolds = numfolds
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.nets = []
        for i in range(numfolds):
            net = FlexNet(structure,sigmoid=False)
            net.load_state_dict(torch.load(f'{networkPath}{i+1}.pth'))
            net.to(self.device)
            self.nets.append(net)
        self.struct = structure

        self.softmax = softmax
        self.sm = torch.nn.Softmax(dim=1)

        #Reads in folds file, then divides the folds up into sets of genes
        foldTable = pd.read_csv(geneFolds).to_numpy()
        self.folds = [{gene[0] for gene in foldTable if gene[1] == i} for i in range(numfolds)]
        self.allGenes = pd.read_csv('./Yeast Resources/GeneSets/BiologicalProcessGenes.csv').values.flatten().tolist()
        self.agnGenes = pd.read_csv('./Yeast Resources/TermPos/AgnosticGenes.csv').to_numpy().flatten()

        self.memMapLen = (sum([len(fold) for fold in self.folds]) * len(self.allGenes) - len(foldTable)) + (len(self.agnGenes) * len(self.allGenes)) - len(set(self.agnGenes) & set(self.allGenes))
        self.foldOffsets = []
        offsetTotal = 0
        for i in range(numfolds):
            self.foldOffsets.append(offsetTotal)
            # offsetTotal += pow(len(self.folds[i]),2)
            offsetTotal += len(self.folds[i]) * len(self.allGenes) - len(self.folds[i])
        self.agnOffset = offsetTotal


    def feedForward(self,fold,term='GO:0007005',trackTime=True,dataset='original',offSet=0,runNegatives=True,calcPos=True,calcAgn=True,saveAll=False,debug=False,resetScores=False,batchSize=50,runBatch=False):
        with torch.no_grad():
            def calcPair(pair):
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device).float()
                outputs = self.nets[fold](features,test=True)
                if self.softmax:
                    outputs = self.sm(outputs)
                
                labels = np.array(labels,dtype=np.intc)
                if saveAll:
                    return np.array(outputs.tolist()[0],dtype='float32')
                else:
                    #offset is an integer that is used to offest the GOTermDict to evaluate on the wrong term
                    return [pair[0],pair[1],outputs[0,self.GOTermDict[term]+offSet].item()]
                
            def calcBatch(batch):
                features, labels = self.makeBatchTensors(np.array(batch))
                features = features.to(self.device).float()
                outputs = self.nets[fold](features,test=True)
                if self.softmax:
                    outputs = self.sm(outputs)
                
                labels = np.array(labels,dtype=np.intc)
                if saveAll:
                    return np.array(outputs.cpu(),dtype='float32')
                else:
                    #offset is an integer that is used to offest the GOTermDict to evaluate on the wrong term
                    return [pair[0],pair[1],outputs[0,self.GOTermDict[term]+offSet].item()]

            if not os.path.exists(f'{self.path}/{self.struct}_Scores.dat') and not(resetScores):
                score_mode = 'w+'
            else:
                score_mode = 'r+'
            if not os.path.exists(f'{self.path}/{self.struct}_Pairs.dat') and not(resetScores):
                pairs_mode = 'w+'
            else:
                pairs_mode = 'r+'
            scoresMemmap = np.memmap(f'{self.path}/{self.struct}_Scores.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode=score_mode)
            pairsMemap = np.memmap(f'{self.path}/{self.struct}_Pairs.dat',shape=(self.memMapLen,2),dtype='U10',mode=pairs_mode)
            
            #Set of all genes that are annotated to tested term
            if os.path.exists(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv'):
                posGenes = pd.read_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv').to_numpy().flatten()
            else:
                posGenes = getGenes(term,dataset=dataset)
                pd.DataFrame(posGenes,columns=['Gene']).to_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv',index=False)
            

            if runNegatives:
                pairs = AllGoGraph.makePairs(self.folds[fold],self.allGenes)
            else:
                pairs = AllGoGraph.makePairs(self.folds[fold],posGenes)


            #agnPairs = AllGoGraph.makePairs(self.folds[fold],agnGenes)
            agnPairs = AllGoGraph.makePairs(self.agnGenes,self.allGenes)
            print(len(agnPairs))

            pairLen = len(pairs)

            if debug:
                pairs = pairs[:5]
                agnPairs = agnPairs[:5]

            if trackTime:
                foldScores = []
                start = time.time()
                if calcPos:
                    if not runBatch:
                        for i,pair in enumerate(pairs,0):
                            scoresMemmap[i+self.foldOffsets[fold],:] = calcPair(pair)
                            pairsMemap[i+self.foldOffsets[fold],:] =  np.array(pair,dtype='U10') 

                            # foldScores.append(calcPair(pair))
                            if i % 10000 == 0 and i != 0:
                                ratio = i/(len(pairs)+len(agnPairs))
                                print(f'Calculated {ratio*100}% of pairs\nTime Spent: {((time.time()-start)/60)}\nEstimated Time Remaining: {((time.time()-start)/60) * ((self.memMapLen - (i+1))) / (i+1)}')
                    else:
                        for i in range(0,len(pairs),batchSize):
                            if i > pairLen - batchSize:
                                batch = pairs[i:]
                                batchOffset = len(batch)
                            else:
                                batch = pairs[i:i+batchSize]
                                batchOffset = batchSize
                            scoresMemmap[i+self.foldOffsets[fold]:i+self.foldOffsets[fold]+batchOffset,:] = calcBatch(batch)
                            pairsMemap[i+self.foldOffsets[fold]:i+self.foldOffsets[fold]+batchOffset,:] =  np.array(batch,dtype='U10') 
                            if i % (10000 / batchSize) == 0 and i != 0:
                                ratio = (i)/len(pairs)
                                print(f'Calculated {ratio*100}% of pairs\nTime Spent: {((time.time()-start)/60)}\nEstimated Time Remaining: {((time.time()-start)/60) * ((self.memMapLen - (i+1))) / (i+1)}')
                    


                agnScores = []
                if calcAgn:
                    if not batch:
                        for i,pair in enumerate(agnPairs,len(pairs)):
                            # agnScores.append(calcPair(pair))
                            scoresMemmap[i+self.agnOffset,:] = scoresMemmap[i+self.agnOffset,:] + (calcPair(pair) / self.numFolds)
                            pairsMemap[i+self.agnOffset,:] = np.array(pair,dtype='U10')
                            if i % 10000 == 0:
                                ratio = (i)/len(pairs)
                                print(f'Calculated {ratio*100}% of pairs\nEstimated Time Remaining: {((time.time()-start)/60) * (((len(pairs)+len(agnPairs)) - (i+i)) / (i+1))}')
                    else:
                        if i > pairLen - batchSize:
                            batch = pairs[i:]
                            batchOffset = len(batch)
                        else:
                            batch = pairs[i:i+batchSize]
                            batchOffset = batchSize
                        scoresMemmap[i+self.agnOffset:i+self.agnOffset+batchOffset,:] = scoresMemmap[i+self.agnOffset:i+self.agnOffset+batchOffset,:] + (calcBatch(batch) / self.numFolds)
                        pairsMemap[i+self.agnOffset:i+self.agnOffset+batchOffset,:] =  np.array(batch,dtype='U10') 
                        if i % (10000 / batchSize) == 0 and i != 0:
                            ratio = (i+self.agnOffset)/len(pairs)
                            print(f'Calculated {ratio*100}% of pairs\nTime Spent: {((time.time()-start)/60)}\nEstimated Time Remaining: {((time.time()-start)/60) * ((self.memMapLen - (i+1))) / (i+1)}')
                    

            else:
                foldScores = [calcPair(pair) for pair in pairs]
                agnScores = [calcPair(pair) for pair in agnPairs]
            
            # if saveAll:
            #     GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').values.tolist()
            #     cols = ['Gene A','Gene B']
            #     for term in GoTerms:
            #         cols.append(term[0])
            # else:
            #     cols = ['Gene A', 'Gene B', 'Score']
            # if calcPos:
            #     pd.DataFrame(foldScores,columns=cols).to_csv(f'{self.path}/posScores_fold{fold}.csv',index=False)
            # if calcAgn:
            #     pd.DataFrame(agnScores,columns=cols).to_csv(f'{self.path}/agnScores_fold{fold}.csv',index=False)


    #rankGenes takes all of the calculated pair scores then ranks the genes by their involvment in a given process
    def rankGenes(self,term='GO:0007005',dataset='original',checkProportion=True):
        
        posGenes = getGenes(term,dataset=dataset)
        leaves = getLeaves(10,dataset=dataset)
        negTerms = [leaf[1] for leaf in leaves if leaf[0] != term]
        negGenes = set()
        for termGenes in negTerms:
            negGenes = negGenes | termGenes
        negGenes = negGenes - set(posGenes)

        termIndex = self.GOTermDict[term]

        scoresMemmap = np.memmap(f'{self.path}/{self.struct}_Scores.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='r+')
        pairsMemMap = np.memmap(f'{self.path}/{self.struct}_Pairs.dat',shape=(self.memMapLen,2),dtype='U10',mode='r+')

        # posGenes = set(pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Pos_original.txt').to_numpy().flatten())
        # negGenes = set(pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Neg_original.txt').to_numpy().flatten())
        # agnGenes = pd.read_csv(f'./Yeast Resources/GeneSets/{term[0:2]}{term[3:]}_Agn_original.txt').to_numpy().flatten()

        def checkPosNeg(gene):
            if gene in posGenes: 
                return 1
            elif gene in negGenes:
                return -1
            else:
                return 0
        
        posSet = set(posGenes)
        # folds = [pd.read_csv(f'{self.path}/posScores_fold{i}.csv').to_numpy(dtype=object) for i in range(self.numFolds)]
        # genePairs = np.concatenate(folds,axis=0)
        # agnFolds = [pd.read_csv(f'{self.path}/agnScores_fold{i}.csv').to_numpy(dtype=object) for i in range(self.numFolds)]
        # agnGenePairs = np.concatenate(agnFolds,axis=0)
        # agnGenes = pd.read_csv('./Yeast Resources/TermPos/AgnosticGenes.csv').to_numpy().flatten()
        
        posScore = {}
        totalScore = {}

        for gene in self.allGenes:
            posScore[gene] = 0
            totalScore[gene] = 0
        for gene in self.agnGenes:
            posScore[gene] = 0
            totalScore[gene] = 0

        # for genePair in genePairs:
        #     totalScore[genePair[0]] = totalScore[genePair[0]] + float(genePair[2])
        #     if genePair[1] in posSet:
        #         posScore[genePair[0]] = posScore[genePair[0]] + float(genePair[2])
        # for genePair in agnGenePairs:
        #     totalScore[genePair[0]] = totalScore[genePair[0]] + (float(genePair[2]) / self.numFolds)
        #     if genePair[1] in posSet:
        #         posScore[genePair[0]] = posScore[genePair[0]] + (float(genePair[2]) / self.numFolds)
        start = time.time()
        for i in range(self.memMapLen):
            if pairsMemMap[i,0] not in posScore or pairsMemMap[i,0] not in totalScore:
                posScore[pairsMemMap[i,0]] = 0
                totalScore[pairsMemMap[i,0]] = 0
            if pairsMemMap[i,1] in posSet:
                posScore[pairsMemMap[i,0]] = posScore[pairsMemMap[i,0]] + scoresMemmap[i,termIndex]
            totalScore[pairsMemMap[i,0]] = totalScore[pairsMemMap[i,0]] + scoresMemmap[i,termIndex]
            if i % 10000 == 0 and i != 0:
                print(f'Calculated {(i/self.memMapLen)*100}% of the pairs\nTime elapsed: {(time.time() - start) / 60}')


        
            
        # if checkProportion:
        #     scoreTable = [[gene,checkPosNeg(gene),(0 if totalScore[gene] == 0 else score/totalScore[gene])] for gene,score in posScore.items()]
        # else:
        #     #scoreTable = [[gene,checkPosNeg(gene),score] for gene,score in posScore.items()]
        #     scoreTable = []
        #     for gene,score in posScore.items():
        #         if score != 0:
        #             scoreTable.append([gene,checkPosNeg(gene),score])
        scoreTable = []
        for gene,score in posScore.items():
            if score != 0:
                scoreTable.append([gene,checkPosNeg(gene),score,totalScore[gene]])
            
        confMat = ConfusionMatrix.calculateMatrix(np.array(scoreTable,dtype=object),1,2)
        pd.DataFrame(confMat,columns=['Gene','Label','Score','Background Score','Precision','Recall','False Positive Rate']).to_csv(f'{self.path}/{self.struct}_GeneRanking_{term[0:2]}{term[3:]}.csv',index=False)

    
    #Makes all possible pairs between 2 sets of genes
    def makePairs(set1,set2):
        pairs = []
        for gene1 in set1:
            for gene2 in set2:
                if gene1 != gene2:
                    pairs.append([gene1,gene2])
        return pairs
