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
from GOParser import GOParser

class AllGoGraph(AllGoModel):
    def __init__(self,networkPath,structure,folder,modelName='',numfolds=4,geneFolds='./src/PairwiseYeastNetwork/AllGOGeneFold_Original_1.csv',singleTermFolds=False,ontologyDataset='modern',memMapName='YeastDict_Regularized.npy',softmax=False,inputVector='x',outputVector='b',addTerms=[]):
        
        #Intialize file path for folder where results will be saved
        self.path = f'./Yeast Resources/GraphResults/{folder}'
        self.modelName = modelName
        
        if(not os.path.exists(self.path)):
            os.mkdir(self.path)

        
        #   The argument 'inputVector' determines what data is included in the input vector of the network based off of what characters are included in 'inputVector'
        #        x - gene expression data
        #        l - localization data
        #        g - genomic interaction data
        #        p - physical interaction data
        
        self.inputSize = 0

        # These four booleans are used for control flow later of data inclusion throughout the Model Object
        self.expression = 'x' in inputVector
        self.localization = 'l' in inputVector
        self.genomicInteraction = 'g' in inputVector
        self.physical = 'p' in inputVector

        if self.expression:
            # Correlations Dictionary that will be retrieve precalculated correlation values
            # self.corrDict = CorrelationDictionary(dictLoc='../YeastMemMap/YeastDict_float16.npy' if (os.path.exists('../YeastMemMap/YeastDict_float16.npy')) else '../YeastDict_float16.npy',datasetType=ontologyDataset)
            self.corrDict = CorrelationDictionary(dictLoc=f'../YeastMemMap/{memMapName}' if (os.path.exists(f'../YeastMemMap/{memMapName}')) else f'../{memMapName}',datasetType=ontologyDataset)
            
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
            if ontologyDataset == 'original':
                interactions = pd.read_csv('./InteractionData.txt',sep="\t").to_numpy()
                interactionsList = pd.read_csv('./GeneticInteractions_Original.csv').to_numpy().flatten()
            else:
                interactions = pd.read_csv('../BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.222.tab.txt',sep="\t").to_numpy()
                interactionsList = pd.read_csv('./GeneticInteractions_Modern.csv').to_numpy().flatten()
            self.genomic_len = len(interactionsList)
                
            # genomic index maps the genomic interactions we care about to an index
            genomicIndex = {item: i for i, item in enumerate(interactionsList)}
            
            self.genomicMap = {}
            for row in interactions:
                # The string of the concatenated gene pair must be stored for both orders of which gene is first
                genePairStrA = row[0] + " " + row[1]
                genePairStrB = row[1] + " " + row[0]
                if (not (genePairStrA in self.genomicMap)) or (not (genePairStrB in self.genomicMap)):
                    self.genomicMap[genePairStrA] = [0 for _ in range(self.genomic_len)]
                    self.genomicMap[genePairStrB] = [0 for _ in range(self.genomic_len)]
                if row[6] in genomicIndex:
                    # If a gene pair has a interaction, change the value of the interactions list for that pair from 0 to 1 at that specific interaction's index
                    tmp = self.genomicMap[genePairStrA]
                    tmp[genomicIndex[row[6]]] = 1
                    self.genomicMap[genePairStrA] = tmp
                    self.genomicMap[genePairStrB] = tmp
            
            self.inputSize += self.genomic_len
                

        if self.physical:
            # Dataset of all bioGRID interactions
            if ontologyDataset == 'original':
                interactions = pd.read_csv('./InteractionData.txt',sep="\t").to_numpy()
                interactionsList = pd.read_csv('./PhysicalInteractions_Original.csv').to_numpy().flatten()
            else:
                interactions = pd.read_csv('../BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-4.4.222.tab.txt',sep="\t").to_numpy()
                interactionsList = pd.read_csv('./PhysicalInteractions_Modern.csv').to_numpy().flatten()
            self.phys_len = len(interactionsList)-2

            
            # physical index maps physical interactions to indicies
            physicalIndex = {item: i for i, item in enumerate(interactionsList[2:])}
            # All types of affinity capture are represented by one node, so they are all mapped to index 0
            physicalIndex['Affinity Capture-MS'] = 0
            physicalIndex['Affinity Capture-Western'] = 0
            
            
            self.physicalMap = {}
            for row in interactions:
                # The string of the concatenated gene pair must be stored for both orders of which gene is first
                genePairStrA = row[0] + " " + row[1]
                genePairStrB = row[1] + " " + row[0]
                if (not (genePairStrA in self.physicalMap)) or (not (genePairStrB in self.physicalMap)):
                    self.physicalMap[genePairStrA] = [0 for _ in range(self.phys_len)]
                    self.physicalMap[genePairStrB] = [0 for _ in range(self.phys_len)]
                if row[6] in physicalIndex:
                    # If a gene pair has a interaction, change the value of the interactions list for that pair from 0 to 1 at that specific interaction's index
                    tmp = self.physicalMap[genePairStrA]
                    tmp[physicalIndex[row[6]]] = 1
                    self.physicalMap[genePairStrA] = tmp
                    self.physicalMap[genePairStrB] = tmp
            
            self.inputSize += self.phys_len


        #   outputVector determines what types of GO terms are included as labels for the output vector
        #       b - Biological Processes
        #       m - Molecular Functions
        #       c - Cellular Components   
        #       n - non specific gene pair interaction (co-annotated to any biological process)    
        #       u - unrelated node (not co-annotated to any biological process)
        #   Additional GO terms can be added with 'addTerm'
        
        self.goParser = GOParser(ontologyDataset)
        self.leaves = self.goParser.getSlimLeaves(cutoff=10,roots=outputVector,onlyLeaves='l' not in outputVector)
        # self.leaves = getLeaves(10,dataset=ontologyDataset,bioProc=('b' in outputVector),molFunc=('m' in outputVector),cellComp=('c' in outputVector),exclude=['GO:0002181','GO:0022857','GO:0032543'])
        for term in addTerms:
            self.leaves.append([term,self.goParser.getGenes(term)])
        self.GOTermDict = {term[0]: i for i,term in enumerate(self.leaves)}
        self.outputSize = len(self.leaves)
        
        self.nonSpecific = 'n' in outputVector
        if self.nonSpecific:
            self.outputSize += 1

        self.unrelated= 'u' in outputVector
        if self.unrelated:
            self.outputSize += 1

        self.randomizeFeatures = False
        self.randomizeLabels = False


        genes = pd.read_csv('./src/PairwiseYeastNetwork/geneIndexDictionary_full.csv').to_numpy()
        self.indexDict = {gene[0]: gene[1] for gene in genes}
        self.geneNum = len(self.indexDict)

        #Intiailize list of networks and device tensor will be calculated on
        self.numFolds = numfolds
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.nets = []
        for i in range(numfolds):
            net = FlexNet(structure,sigmoid=False)
            if os.path.exists(f'{networkPath}{i+1}.pth'):
                net.load_state_dict(torch.load(f'{networkPath}{i+1}.pth'))
            net.to(self.device)
            self.nets.append(net)
        self.struct = structure

        self.softmax = softmax
        self.sm = torch.nn.Softmax(dim=1)

        #Reads in folds file, then divides the folds up into sets of genes
        foldTable = pd.read_csv(geneFolds).to_numpy()

        # Single term folds specify fold number in the column 2 while AllGO folds specify number in column 1
        if singleTermFolds:
            self.folds = [{gene[0] for gene in foldTable if gene[2] == i} for i in range(numfolds)]
        else:
            self.folds = [{gene[0] for gene in foldTable if gene[1] == i} for i in range(numfolds)]
        # self.allGenes = pd.read_csv('./Yeast Resources/GeneSets/BiologicalProcessGenes.csv').values.flatten().tolist()
        self.allGenes = list(self.goParser.onto.yorfs.keys())
        self.foldGenes = [gene[0] for gene in foldTable]

        negTerms = [leaf[1] for leaf in self.leaves]
        negGenes = set()
        for termGenes in negTerms:
            negGenes = negGenes | termGenes

        self.agnGenes = set(self.allGenes) - negGenes

        # self.memMapLen = (sum([len(fold) for fold in self.folds]) * len(self.allGenes) - len(foldTable)) + (len(self.agnGenes) * len(self.allGenes)) - len(set(self.agnGenes) & set(self.allGenes))
        self.memMapLen(len(foldTable)*len(foldTable)-len(foldTable)) + (len(self.agnGenes)*len(self.allGenes)-len(self.agnGenes))
        self.foldOffsets = []
        offsetTotal = 0
        for i in range(numfolds):
            self.foldOffsets.append(offsetTotal)
            offsetTotal += len(self.folds[i]) * len(self.allGenes) - len(self.folds[i])
        self.agnOffset = offsetTotal


    def feedForward(self,fold,term='GO:0007005',dataset='original',calcPos=True,calcAgn=True,saveAll=True,debug=False,resetScores=False,batchSize=50,printProgress=False,partition=False,partNum=0,calcPart=0):
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
                    return [pair[0],pair[1],outputs[0,self.GOTermDict[term]].item()]
                
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
                    return [batch[0],batch[1],outputs[0,self.GOTermDict[term]].item()]

            if not os.path.exists(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores.dat') and not(resetScores):
                score_mode = 'w+'
            else:
                score_mode = 'r+'
            if not os.path.exists(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs.dat') and not(resetScores):
                pairs_mode = 'w+'
            else:
                pairs_mode = 'r+'
            scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode=score_mode)
            pairsMemap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs.dat',shape=(self.memMapLen,2),dtype='U10',mode=pairs_mode)
            
            #Set of all genes that are annotated to tested term
            if os.path.exists(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv') and False:
                posGenes = pd.read_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv').to_numpy().flatten()
            else:
                posGenes = getGenes(term,dataset=dataset)
                # pd.DataFrame(posGenes,columns=['Gene']).to_csv(f'./Yeast Resources/TermPos/GO-{term[3:]}_Pos_{dataset}.csv',index=False)
            
            self.nets[fold].eval()
            
            
            pairs = AllGoGraph.makePairs(self.folds[fold],self.foldGenes)
            agnPairs = AllGoGraph.makePairs(self.agnGenes,self.allGenes)
            
        
            pairLen = len(pairs)
            
            agnLen = len(agnPairs)
            

            if debug:
                pairs = pairs[:5]
                agnPairs = agnPairs[:5]

            
            start = time.time()

            if partition:
                posPart = int(len(pairs)/partNum)
                posStart = calcPart * posPart
                posEnd = (calcPart+1) * posPart if calcPart + 1 != partNum else len(pairs)
                posRange = range(posStart,posEnd,batchSize)

                agnPart = int(len(agnPairs)/partNum)
                agnStart = calcPart * agnPart
                agnEnd = (calcPart+1) * agnPart if calcPart + 1 != partNum else len(agnPairs)
                agnRange = range(agnStart,agnEnd,batchSize)
            else:
                posRange = range(0,len(pairs),batchSize)
                agnRange = range(0,len(agnPairs),batchSize)

            if calcPos:
            
                for i in posRange:
                    if i > pairLen - batchSize:
                        
                        batch = pairs[i:]
                        batchOffset = len(batch)
                        
                    else:
                        
                        batch = pairs[i:i+batchSize]
                        batchOffset = batchSize
                    scoresMemmap[i+self.foldOffsets[fold]:i+self.foldOffsets[fold]+batchOffset,:] = calcBatch(batch)
                    pairsMemap[i+self.foldOffsets[fold]:i+self.foldOffsets[fold]+batchOffset,:] =  np.array(batch,dtype='U10') 
                    if i % (10000 / batchSize) == 0 and i != 0 and printProgress:
                        ratio = (i)/len(pairs)
                        print(f'Calculated {ratio*100}% of pairs\nTime Spent: {((time.time()-start)/60)}\nEstimated Time Remaining: {((time.time()-start)/60) * ((self.memMapLen - (i+1))) / (i+1)}')
                
            if calcAgn:
            
                print("Start Agn")
                for i in agnRange:
                    if i > agnLen - batchSize:
                        batch = agnPairs[i:]
                        batchOffset = len(batch)
                    else:
                        batch = agnPairs[i:i+batchSize]
                        batchOffset = batchSize
                    scoresMemmap[i+self.agnOffset:i+self.agnOffset+batchOffset,:] = scoresMemmap[i+self.agnOffset:i+self.agnOffset+batchOffset,:] + (calcBatch(batch) / self.numFolds)
                    pairsMemap[i+self.agnOffset:i+self.agnOffset+batchOffset,:] =  np.array(batch,dtype='U10') 
                    if i % (10000 / batchSize) == 0 and i != 0 and printProgress:
                        ratio = (i+self.agnOffset)/len(pairs)
                        print(f'Calculated {ratio*100}% of pairs\nTime Spent: {((time.time()-start)/60)}\nEstimated Time Remaining: {((time.time()-start)/60) * ((self.memMapLen - (i+1))) / (i+1)}')


    #rankGenes takes all of the calculated pair scores then ranks the genes by their involvment in a given process
    def rankGenes(self,term='GO:0007005',dataset='original',checkProportion=True,sigmoid=False,agn=True,fileSuffix=""):
        
        posGenes = self.goParser.getGenes(term)
        negTerms = [leaf[1] for leaf in self.leaves if leaf[0] != term]
        negGenes = set()
        for termGenes in negTerms:
            negGenes = negGenes | termGenes
        negGenes = negGenes - set(posGenes)

        termIndex = self.GOTermDict[term]

        scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='r+')
        pairsMemMap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs.dat',shape=(self.memMapLen,2),dtype='U10',mode='r+')


        def checkPosNeg(gene):
            if gene in posGenes: 
                return 1
            elif gene in negGenes:
                return -1
            else:
                return 0
        
        posSet = set(posGenes)
        
        posScore = {}
        totalScore = {}

        for gene in self.allGenes:
            posScore[gene] = 0
            totalScore[gene] = 0
        for gene in self.agnGenes:
            posScore[gene] = 0
            totalScore[gene] = 0


        start = time.time()
        pairsRange = self.memMapLen if agn else self.agnOffset
        for i in range(pairsRange):
            score = 1.0 / (1.0+ np.exp(-scoresMemmap[i,termIndex])) if sigmoid else scoresMemmap[i,termIndex]
            if pairsMemMap[i,0] not in posScore or pairsMemMap[i,0] not in totalScore:
                posScore[pairsMemMap[i,0]] = 0
                totalScore[pairsMemMap[i,0]] = 0
            if pairsMemMap[i,1] in posSet:
                posScore[pairsMemMap[i,0]] = posScore[pairsMemMap[i,0]] + score
            totalScore[pairsMemMap[i,0]] = totalScore[pairsMemMap[i,0]] + score
            if i % 10000 == 0 and i != 0 and False:
                print(f'Calculated {(i/self.memMapLen)*100}% of the pairs\nTime elapsed: {(time.time() - start) / 60}')


        
        
        scoreTable = []
        for gene,score in posScore.items():
            if score != 0:
                scoreTable.append([gene,checkPosNeg(gene),score,totalScore[gene]])
        scoreTable_filt = list(filter(lambda row: row[1] != 0,scoreTable))
            
        confMat = np.array(ConfusionMatrix.calculateMatrix(np.array(scoreTable,dtype=object),1,2),dtype=object)
        confMat_filt = np.array(ConfusionMatrix.calculateMatrix(np.array(scoreTable_filt,dtype=object),1,2),dtype=object)
        pd.DataFrame(confMat,columns=['Gene','Label','Score','Background Score','Precision','Recall','False Positive Rate']).to_csv(f'{self.path}/{"" if self.modelName == "" else f"_{self.modelName}"}{self.struct}_GeneRanking_{term[0:2]}{term[3:]}{"_sigmoid" if sigmoid else ""}{fileSuffix}.csv',index=False)
        return (np.mean(confMat_filt[:,5]),AllGoGraph.averagePrecision(confMat_filt[:,4]))
    
    def rankAllTerms(self,dataset='original'):
        summary = []
        for term,index in self.GOTermDict.items():
            auc, avgPrec = self.rankGenes(term=term,dataset=dataset)
            summary.append([term,auc,avgPrec])
        pd.DataFrame(summary,columns=['GO Term','AUC','Average Precision']).to_csv(f'{self.path}/{"" if self.modelName == "" else f"_{self.modelName}"}GOTermDistribution.csv',index=False)

    # Used to caculate convex hull average precision
    def averagePrecision(inputArray):
                precisionArray = np.copy(inputArray)
                for i in range(len(precisionArray)-1,0,-1):
                    if precisionArray[i] > precisionArray[i-1]:
                        precisionArray[i-1] = precisionArray[i]
                return np.mean(precisionArray)
    
    def makeGraph(self):
        print(f'{self.path}/{self.struct}_Scores.dat')
        print(os.path.exists(f'{self.path}/{self.struct}_Scores.dat'))
        print(f'{self.path}/{self.struct}_Pairs.dat')
        print(os.path.exists(f'{self.path}/{self.struct}_Pairs.dat'))
        if not(os.path.exists(f'{self.path}/{self.struct}_Scores.dat') and os.path.exists(f'{self.path}/{self.struct}_Pairs.dat')):
            print('Pairs have not been calculated yet')
        else:
            scoresMemmap = np.memmap(f'{self.path}/{self.struct}_Scores.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='r+')
            pairsMemap = np.memmap(f'{self.path}/{self.struct}_Pairs.dat',shape=(self.memMapLen,2),dtype='U10',mode='r+')
            graph = np.zeros(shape=(len(self.leaves),sum(range(len(self.allGenes+1)))),dtype=np.float16)
            for i in range(len(pairsMemap)):
                graph[:,self.calcIndex(pairsMemap[i,0],pairsMemap[i,1])] += scoresMemmap[i,:] / 2
            np.save(f'{self.path}/Graph.npy',arr=graph)


    def calcIndex(self,gene1,gene2):
        if self.indexDict[gene1] > self.indexDict[gene2]:
            row = self.indexDict[gene1]
            col = self.indexDict[gene2]
        else:
            col = self.indexDict[gene1]
            row = self.indexDict[gene2]
        return (col * self.geneNum - sum(range(col))) + row


    
    #Makes all possible pairs between 2 sets of genes
    def makePairs(set1,set2):
        pairs = []
        for gene1 in set1:
            for gene2 in set2:
                if gene1 != gene2:
                    pairs.append([gene1,gene2])
        return pairs
    
