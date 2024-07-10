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
    def __init__(self,networkPath,structure,folder,modelName='',numfolds=4,geneFolds='./src/PairwiseYeastNetwork/AllGOGeneFold_Original_1.csv',singleTermFolds=False,ontologyDataset='2007',evalDataset='2007',memMapName='YeastDict_Regularized.npy',softmax=False,inputVector='x',outputVector='b',addTerms=[]):
        
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


        self.inputVector = inputVector
        self.outputVector = outputVector

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

        self.evalParser = GOParser(evalDataset)
        self.evalLeaves = self.evalParser.getSlimLeaves(cutoff=10,roots=self.outputVector,onlyLeaves='l' not in self.outputVector)
        
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
        
        self.allGenes = set(self.goParser.onto.yorfs.keys())
        
        self.foldGenes = {gene[0] for gene in foldTable}

        negTerms = [leaf[1] for leaf in self.leaves]
        negGenes = set()
        for termGenes in negTerms:
            negGenes = negGenes | termGenes

        self.agnGenes = set(self.allGenes) - negGenes

        genes = list(self.allGenes)
        genes.sort()
        self.geneIndex = {}
        for (i, gene) in enumerate(genes):
            self.geneIndex[gene] = i

        print("Neg genes:",len(negGenes))
        print("Fold table:",len(foldTable))
        print("Fold table:",sum([len(fold) for fold in self.folds]))
        print("Agn genes:",len(self.agnGenes))
        print("Intersection:",len(self.agnGenes & self.allGenes))

        
        

        
        self.memMapLen = (len(foldTable)*len(foldTable)-len(foldTable)) + (len(self.agnGenes)*len(self.allGenes)-len(self.agnGenes))
        
        self.foldMemMapLen = [(len(self.folds[i]) * len(foldTable) - len(self.folds[i])) + (len(self.agnGenes)*len(self.allGenes)-len(self.agnGenes)) for i in range(numfolds)]
        self.foldMemMapLen_anno = [(len(self.folds[i]) * len(foldTable) - len(self.folds[i])) for i in range(numfolds)]
        self.agnLen = (len(self.agnGenes)*len(self.allGenes)-len(self.agnGenes))
        # self.foldLens = []
        # offsetTotal = 0
        # for i in range(numfolds):
        #     self.foldOffsets.append(offsetTotal)
        #     offsetTotal += len(self.folds[i]) * len(foldTable) - len(self.folds[i])
        # self.agnOffset = offsetTotal
        


    def feedForward(self,fold,term='GO:0007005',dataset='original',calcPos=True,calcAgn=True,saveAll=True,debug=False,resetScores=False,batchSize=50,printProgress=False,partition=False,partNum=0,calcPart=0,flush=False):
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

            if not os.path.exists(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores_fold{fold}.dat') and not(resetScores):
                score_mode = 'w+'
            else:
                score_mode = 'r+'
            if not os.path.exists(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs_fold{fold}.dat') and not(resetScores):
                pairs_mode = 'w+'
            else:
                pairs_mode = 'r+'
            scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores_fold{fold}.dat',dtype='float32',shape=(self.foldMemMapLen[fold],len(self.leaves)),mode=score_mode)
            pairsMemap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs_fold{fold}.dat',shape=(self.foldMemMapLen[fold],2),dtype='U10',mode=pairs_mode)
            
                
            
            self.nets[fold].eval()
            
            
            pairs = AllGoGraph.makePairs(self.folds[fold],self.foldGenes)
            agnPairs = AllGoGraph.makePairs(self.agnGenes,self.allGenes)
            
        
            pairLen = len(pairs)
            
            agnLen = len(agnPairs)
            

            if debug:
                pairs = pairs[:5]
                agnPairs = agnPairs[:5]

            
            start = time.time()

            # if partition:
            #     posPart = int(len(pairs)/partNum)
            #     posStart = calcPart * posPart
            #     posEnd = (calcPart+1) * posPart if calcPart + 1 != partNum else len(pairs)
            #     posRange = range(posStart,posEnd,batchSize)

            #     agnPart = int(len(agnPairs)/partNum)
            #     agnStart = calcPart * agnPart
            #     agnEnd = (calcPart+1) * agnPart if calcPart + 1 != partNum else len(agnPairs)
            #     agnRange = range(agnStart,agnEnd,batchSize)
            # else:
            posRange = range(0,len(pairs),batchSize)
            agnRange = range(0,len(agnPairs),batchSize)

            if calcPos:
            
                for i in posRange:
                    if i > pairLen - batchSize:
                        
                        batch = pairs[i:]
                        print(batch)
                        batchOffset = len(batch)
                        
                    else:
                        
                        batch = pairs[i:i+batchSize]
                        batchOffset = batchSize
                    scoresMemmap[i:i+batchOffset,:] = calcBatch(batch)
                    pairsMemap[i:i+batchOffset,:] =  np.array(batch,dtype='U10') 
                        
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
                    scoresMemmap[i+pairLen:i+pairLen+batchOffset,:] = (calcBatch(batch) / self.numFolds)
                    pairsMemap[i+pairLen:i+pairLen+batchOffset,:] =  np.array(batch,dtype='U10') 
                    if i % (10000 / batchSize) == 0 and i != 0 and printProgress:
                        ratio = (i+self.agnOffset)/len(pairs)
                        print(f'Calculated {ratio*100}% of pairs\nTime Spent: {((time.time()-start)/60)}\nEstimated Time Remaining: {((time.time()-start)/60) * ((self.memMapLen - (i+1))) / (i+1)}')
            scoresMemmap.flush()
            pairsMemap.flush()


    #rankGenes takes all of the calculated pair scores then ranks the genes by their involvment in a given process
    def rankGenes(self,term='GO:0007005',sigmoid=False,agn=True,fileSuffix="",singleTerm=False,modern=False):
        
        
        posGenes = self.goParser.getGenes(term)
        evalPosGenes = self.evalParser.getGenes(term)
        

        negGenes = set()
        evalNegGenes = set()
        
        if not singleTerm:
            negTerms = [leaf[1] for leaf in self.leaves if leaf[0] != term]
            for termGenes in negTerms:
                negGenes = negGenes | termGenes
            negGenes = negGenes - set(posGenes)

            evalNegTerms = [leaf[1] for leaf in self.evalLeaves if leaf[0] != term]
            for termGenes in evalNegTerms:
                evalNegGenes = evalNegGenes | termGenes
            evalNegGenes = evalNegGenes - set(evalPosGenes)

        else:
            negGenes = set(self.foldGenes) - posGenes
            evalNegGenes = set(self.foldGenes) - evalPosGenes

        termIndex = self.GOTermDict[term]

        

        def checkPosNeg(gene):
            if gene in posGenes: 
                return 1
            elif gene in negGenes:
                return -1
            else:
                return 0
            
        def checkPosNegEval(gene):
            if gene in evalPosGenes:
                return 1
            elif gene in evalNegGenes:
                return -1
            else:
                return 0

            
        def annoCompare(gene):
            if gene in posGenes:
                ogAnno = '+'
            elif gene in negGenes:
                ogAnno = '-'
            else:
                ogAnno = '0'
            
            if gene in evalPosGenes:
                modAnno = '+'
            elif gene in evalNegGenes:
                modAnno = '-'
            else:
                modAnno = '0'

            return ogAnno + '/' + modAnno
        
        posSet = set(posGenes)
        
        posScore = {}
        totalScore = {}
        numScores = {}
        nonGenes = {}

        for gene in self.allGenes:
            posScore[gene] = 0
            totalScore[gene] = 0
            numScores[gene] = 0
        for gene in self.agnGenes:
            posScore[gene] = 0
            totalScore[gene] = 0
            numScores[gene] = 0


        start = time.time()
        

        for fold in range(self.numFolds):
            scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores_fold{fold}.dat',dtype='float32',shape=(self.foldMemMapLen[fold],len(self.leaves)),mode='r+')
            pairsMemMap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs_fold{fold}.dat',shape=(self.foldMemMapLen[fold],2),dtype='U10',mode='r+')

            for i in range(self.foldMemMapLen[fold]):
                score = 1.0 / (1.0+ np.exp(-scoresMemmap[i,termIndex])) if sigmoid else scoresMemmap[i,termIndex]
                
                if pairsMemMap[i,0] not in posScore or pairsMemMap[i,0] not in totalScore or pairsMemMap[i,0] not in numScores:
                    if pairsMemMap[i,0] not in nonGenes:
                        nonGenes[pairsMemMap[i,0]] = 0
                    nonGenes[pairsMemMap[i,0]] += 1
                
                if pairsMemMap[i,1] in posSet:
                    posScore[pairsMemMap[i,0]] = posScore[pairsMemMap[i,0]] + score
                    numScores[pairsMemMap[i,0]] = numScores[pairsMemMap[i,0]] + 1
                totalScore[pairsMemMap[i,0]] = totalScore[pairsMemMap[i,0]] + score
            
            
        # pd.DataFrame([[gene,num] for gene,num in nonGenes.items()],columns=['Genes','Occurences']).to_csv('NonGenes.csv',index=False)

        
        
        scoreTable = []
        for gene,score in posScore.items():
            
            if score != 0:
                label =  checkPosNegEval(gene) if modern else checkPosNeg(gene)
                scoreTable.append([gene,label,annoCompare(gene),score,totalScore[gene],numScores[gene]])
        scoreTable_filt = list(filter(lambda row: row[1] != 0,scoreTable))
            
        confMat = np.array(ConfusionMatrix.calculateMatrix(np.array(scoreTable,dtype=object),1,3),dtype=object)
        confMat_filt = np.array(ConfusionMatrix.calculateMatrix(np.array(scoreTable_filt,dtype=object),1,3),dtype=object)
        pd.DataFrame(confMat,columns=['Gene','Label','Annos','Score','Background Score','Num pos pairs','Precision','Recall','False Positive Rate']).to_csv(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}"}{self.struct}_GeneRanking_{term[0:2]}{term[3:]}{"_sigmoid" if sigmoid else ""}{fileSuffix}.csv',index=False)
        return (np.mean(confMat_filt[:,7]),AllGoGraph.averagePrecision(confMat_filt[:,6]))
    
    def rankAllTerms(self,agn=True,fileSuffix='',modern=False):
        summary = []
        for term,index in self.GOTermDict.items():
            auc, avgPrec = self.rankGenes(term=term,agn=agn,fileSuffix=fileSuffix,modern=modern)
            summary.append([term,auc,avgPrec])
        pd.DataFrame(summary,columns=['GO Term','AUC','Average Precision']).to_csv(f'{self.path}/{"" if self.modelName == "" else f"_{self.modelName}"}{self.struct}GOTermDistribution{fileSuffix}.csv',index=False)

    # Used to caculate convex hull average precision
    def averagePrecision(inputArray):
                precisionArray = np.copy(inputArray)
                for i in range(len(precisionArray)-1,0,-1):
                    if precisionArray[i] > precisionArray[i-1]:
                        precisionArray[i-1] = precisionArray[i]
                return np.mean(precisionArray)
    
    def makeGraph(self):
        scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores_Combined.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='r+')
        pairsMemMap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs_Combined.dat',shape=(self.memMapLen,2),dtype='U10',mode='r+')

        n = len(self.allGenes)
        graphSize = int((n*(n-1))/2)
        graphs = np.zeros((len(self.leaves),graphSize),dtype='float16')

        for i in range(self.memMapLen):
            gi = self.graphIndex(pairsMemMap[i,0],pairsMemMap[i,1])
            graphs[:,gi] += scoresMemmap[i,:] / 2
        np.save(f'{self.modelName}_{self.struct}_Graph.npy',graphs)

        


    def sampleGraph(self,folder,sampleSize=100000):
        graphs = np.load(f'{self.modelName}_{self.struct}_Graph.npy')

        if not os.path.exists(f'./Yeast Resources/PairsSample/{folder}'):
            os.mkdir(f'./Yeast Resources/PairsSample/{folder}')

        for term, genes in self.leaves:
            termPairs = graphs[self.GOTermDict[term],:]
            samp = np.random.choice(termPairs,sampleSize,replace=False)
            pd.DataFrame(samp,columns=['Scores']).to_csv(f'./Yeast Resources/PairsSample/{folder}/{term[0:2]}-{term[3:]}_PairsSample.csv',index=False)

    def queryConnections(self,querySet):
        table = []

        for gene in (self.allGenes - set(querySet)):
            for term, termGenes in self.leaves:
                for qGene in querySet:
                    pass

        

    def graphIndex(self,geneA,geneB):
            if geneA < geneB: # If a comes alphabetically before B
                row = self.geneIndex[geneA]
                col = self.geneIndex[geneB]
            else:
                row = self.geneIndex[geneB]
                col = self.geneIndex[geneA]
            n = len(self.allGenes)
            i = row * ((n-1) - ((row-1)/2)) + (col - row - 1)
            return i
            
        



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
    
    def combineScores(self):
        print('Combining Graphcs')



        scoresMemmap_combined = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores_Combined.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='w+')
        pairsMemMap_combined = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs_Combined.dat',shape=(self.memMapLen,2),dtype='U10',mode='w+')
        agnStart = self.memMapLen-self.agnLen
        offset = 0
        for fold in range(self.numFolds):
            scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores_fold{fold}.dat',dtype='float32',shape=(self.foldMemMapLen[fold],len(self.leaves)),mode='r+')
            pairsMemMap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs_fold{fold}.dat',shape=(self.foldMemMapLen[fold],2),dtype='U10',mode='r+')

            for i in range(self.foldMemMapLen_anno[fold]):
                scoresMemmap_combined[i+offset,:] = scoresMemmap[i,:]
                pairsMemMap_combined[i+offset,:] = pairsMemMap[i,:]
            offset += self.foldMemMapLen_anno[fold]

            for i in range(self.agnLen):
                scoresMemmap_combined[i+agnStart,:] += (scoresMemmap[i+self.foldMemMapLen_anno[fold]])
                pairsMemMap_combined[i+agnStart,:] = pairsMemMap[i+self.foldMemMapLen_anno[fold]] 

    def termSample(self,folder,sampleSize=100000):
        if not os.path.exists(f'./Yeast Resources/PairsSample/{folder}'):
            os.mkdir(f'./Yeast Resources/PairsSample/{folder}')
        scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores_Combined.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='r+')
        pairsMemMap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs_Combined.dat',shape=(self.memMapLen,2),dtype='U10',mode='r+')
        for term, genes in self.leaves:
            termPairs = scoresMemmap[:,self.GOTermDict[term]]
            samp = np.random.choice(termPairs,sampleSize,replace=False)
            pd.DataFrame(samp,columns=['Scores']).to_csv(f'./Yeast Resources/PairsSample/{folder}/{term[0:2]}-{term[3:]}_PairsSample.csv',index=False)

            






            
    
    def to_csv(self,loc):
        scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='r+')
        pairsMemMap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs.dat',shape=(self.memMapLen,2),dtype='U10',mode='r+')

        table = np.concatenate([scoresMemmap,pairsMemMap],axis=1,dtype=object)
        pd.DataFrame(table,columns=['Gene_A','Gene_B']+[leaf[0] for leaf in self.leaves]).to_csv(loc,index=False)



    def debug(self):
        scoresMemmap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Scores.dat',dtype='float32',shape=(self.memMapLen,len(self.leaves)),mode='r+')
        pairsMemMap = np.memmap(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}_"}{self.struct}_Pairs.dat',shape=(self.memMapLen,2),dtype='U10',mode='r+')

        pairs = AllGoGraph.makePairs(self.foldGenes,self.foldGenes)
        agnPairs = AllGoGraph.makePairs(self.agnGenes,self.allGenes)
        

        # batch = pairs[-50:]
        # print(batch)
        # print(np.array(batch,dtype='U10') )

        numPairs = {}
        for gene in self.allGenes:
            numPairs[gene] = 0

        for i in range(len(pairs)):
            numPairs[pairs[i][0]] += 1
            numPairs[pairs[i][1]] += 1
        for i in range(len(agnPairs)):
            numPairs[agnPairs[i][0]] += 1
            numPairs[agnPairs[i][1]] += 1

        occur = {}
        for i in range(len(pairsMemMap)):
            if pairsMemMap[i,0] not in occur:
                occur[pairsMemMap[i,0]] = 0
            if pairsMemMap[i,1] not in occur:
                occur[pairsMemMap[i,1]] = 0
            occur[pairsMemMap[i,0]] += 1
            occur[pairsMemMap[i,1]] += 1

        def membership(gene):
            if gene in self.foldGenes:
                return "Annotated"
            elif gene in self.agnGenes:
                return "Agnostic"
            else:
                return "Corrupted"

        occurLst = [(gene,num,membership(gene)) for gene,num in occur.items()]
        occurLst.sort(key=(lambda x: x[1]))

        pairsLst = [(gene,num,membership(gene)) for gene, num in numPairs.items()]
        pairsLst.sort(key=(lambda x: x[1]))
        pd.DataFrame(occurLst,columns=["Gene","Occurences in MemMap Pairs","Membership"]).to_csv(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}"}{self.struct}_MemMapOccur.csv',index=False)
        pd.DataFrame(pairsLst,columns=["Gene","Occurances in pairs","Membership"]).to_csv(f'{self.path}/{"" if self.modelName == "" else f"{self.modelName}"}{self.struct}_PairsOccurences.csv',index=False)

    

    def generateAllGenes(self):
        pd.DataFrame(self.allGenes,columns=['Genes']).to_csv('AllGenes.csv',index=False)
        




    
