from random import random
from CorrelationDictionary import CorrelationDictionary
import pandas as pd
import numpy as np
from FlexNet import FlexNet
import torch
import time
import os
import random
from FocalLoss import FocalLoss
from CustomCrossEntropyLoss import CustomCrossEntropyLoss
import threading

from scipy import stats


import sys
from YeastDataFile import YeastDataFile

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes


class AllGoModel():
    def __init__(self,fold,structure,folderName,modelName,numFolds=4,lr=0.01,min_lr=1e-7,momentum=0.9,batch=50,gamma=2,alpha=1,weighted=False,lossFunc='CE',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='modern',regularize=True,inputDropout=None,hiddenDropout=None,activation='relu',resetNet=False,cuda=True,inputVector = 'xl',outputVector = 'b',addTerms=[],memMapName='YeastDict_Redo.dat'):
        # Handling what data is in the input and output vector of the vector

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
        #       n - non specific gene pair interaction (co-annotated to any biological process)    
        #   Additional GO terms can be added with 'addTerm'
        
        self.leaves = getLeaves(10,dataset=ontologyDataset,bioProc=('b' in outputVector),molFunc=('m' in outputVector),cellComp=('c' in outputVector))
        for term in addTerms:
            self.leaves.append([term,set(getGenes(term,dataset=ontologyDataset))])
        self.GOTermDict = {term[0]: i for i,term in enumerate(self.leaves)}
        self.outputSize = len(self.leaves)
        
        self.nonSpecific = 'n' in outputVector
        if self.nonSpecific:
            self.outputSize += 1
        
        
        
        
        if foldFile or 'original' or foldFile == 'Original' or foldFile == '2009':
            foldFile = './src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv'
        elif foldFile == 'modern' or foldFile == 'Modern' or foldFile == '2023':
            foldFile = './src/PairwiseYeastNetwork/AllGOGeneFold1.csv'


        # If the foldFile does not exit, make new gene folds; Otherwise, generate val and training data from the foldFile
        if not os.path.exists(foldFile):
            folds = self.makeNewGeneFolds(foldFile=foldFile)
        else:
            #Read in file of gene folds
            folds = pd.read_csv(foldFile).to_numpy()

       
        
        self.validation = np.array([gene[0] for gene in folds if gene[1] == fold],dtype='U10')
        self.training = np.array([gene[0] for gene in folds if gene[1] != fold],dtype='U10')
        np.random.shuffle(self.training)
        print('Initialized training and validation data')


        # Instance variables
        self.batch = batch
        self.lr = lr
        self.fold = fold
        self.regularize = regularize
        self.numFolds = numFolds
        self.folds = folds


        # Neural Network code
        inputDrop_name = '' if inputDropout == None or inputDropout == 0 else f'_inputDrop{inputDropout}'
        hiddenDrop_name = '' if hiddenDropout == None or hiddenDropout == 0 else f'_hiddenDrop{hiddenDropout}'

        lr_name = '' if lr == 0.001 else f'_lr{lr}'
        batch_name = '' if batch == 500 else f'_batch{batch}'
        lf_name = '' if lossFunc == 'CE' else f'_lf{lossFunc}'
        momentum_name = '' if momentum == 0.9 else f'_momentum{momentum}'
        alpha_name = '' if alpha == 1 else f'_alpha{alpha}'
        gamma_name = '' if gamma == 2 else f'_gamma{gamma}'

        input_name = ''.join(sorted(inputVector))
        output_name = ''.join(sorted(outputVector))

        struct = f'{self.inputSize}x{structure}x{self.outputSize}'

        model_specification = f'{modelName}_{input_name}_{output_name}_{struct}{lr_name}{batch_name}{lf_name}{momentum_name}{alpha_name}{gamma_name}{inputDrop_name}{hiddenDrop_name}'

        
        #Initialize the network, the size of the input layer is the number of expression datasets, and the size of the output is the number of leaf go terms
        self.networkLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{model_specification}_Net_fold{self.fold+1}.pth'
        
        if inputDropout == 0:
            inputDropout = None
        if hiddenDropout == 0:
            hiddenDropout = None

        self.resetNet = resetNet
        

        self.net = FlexNet(struct,sigmoid=False,activation=activation,inputDrop=inputDropout,hiddenDrop=hiddenDropout)
        if(os.path.exists(self.networkLoc) and not(resetNet)):
            self.net.load_state_dict(torch.load(self.networkLoc))
        
        #Choose which device to run network on, then move network to that device
        self.device = 'cuda:0' if torch.cuda.is_available() and cuda else 'cpu'
        self.net.to(self.device)
        print('Initialized Network')

        if weighted:
            # Formula for the weight of each GO term is (N^2/n^2) where:
            #   N - the total number of genes across all fold
            #   n - the number of gene annotated to a given go term
            # Weights are then divided by the sum of weights so that they add to zero, then they are multiplied by the number of output nodes
            self.weights = torch.tensor([pow(len(folds),2) / pow(len(leaf[1]),2) for leaf in self.leaves],dtype=torch.float) 
            self.weights = (self.weights / torch.sum(self.weights)) * len(self.leaves)

        else:
            self.weights = torch.ones((len(self.leaves),),dtype=float)
        
        self.weights = self.weights.to(self.device)
        

        #Initialize Loss function, we are using CEL because we have multiple outputs that could be true
        if lossFunc in ['CE','crossEntropy','cross_entropy']:
            # self.lossFunc = torch.nn.CrossEntropyLoss()
            self.lossFunc = CustomCrossEntropyLoss(alpha=self.weights,nonSpecific='n' in outputVector)
            print('Used Cross Entropy Loss Function')
        elif lossFunc in ['WCE','weightedCrossEntropy','weighted_cross_entropy']:
            self.lossFunc = torch.nn.CrossEntropyLoss(weight=self.weights)
            print('Used Weighted Cross Entropy Loss Function')
        elif lossFunc in ['FL','focalLoss','focal_loss']:
            self.lossFunc = FocalLoss(gamma=gamma,alpha=self.weights,nonSpecific='n' in outputVector)
        elif lossFunc in ['BCE','binaryCrossEntropy','binary_cross_entropy']:
            self.lossFunc = torch.nn.BCEWithLogitsLoss(weight=self.weights)
        else:
            # self.lossFunc = torch.nn.CrossEntropyLoss(reduction='mean')
            self.lossFunc = CustomCrossEntropyLoss(alpha=self.weights,nonSpecific='n' in outputVector)
            print('Used Cross Entropy Loss Function')
        
        
        #Stochastic Gradient Descent Optimizer
        self.opt = torch.optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)
        self.scheduler = torch.optim.lr_scheduler.CyclicLR(self.opt,base_lr=min_lr,max_lr=lr,step_size_up=10000,step_size_down=10000)

        

        # This section of is used to determine what names networks, losses, and testing data are saved under
        # The general pattern is that if a parameter diverges from the norm, its value is included in the filename
        
    

        self.lossLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{model_specification}_Loss_fold{self.fold+1}.csv'
        #The locations for the testing and training data will be folder because they will be storing a csv file for each GO term
        self.trainLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{model_specification}_Train_/'
        self.testLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{model_specification}_Test_/'
        print(self.trainLoc)
        print(self.testLoc)

        #These three conditional check if the folder that the output data will be stored exist, and if not, construct those folders
        if not os.path.exists(f'./Yeast Resources/Pairwise/Spell/{folderName}'):
            os.mkdir(f'./Yeast Resources/Pairwise/Spell/{folderName}')
        
        if not os.path.exists(self.testLoc):
            os.mkdir(self.testLoc)

        if not os.path.exists(self.trainLoc):
            os.mkdir(self.trainLoc)

        if not os.path.exists(f'./Yeast Resources/Pairwise/Spell/{folderName}/{model_specification}_specification.txt'):
            f = open(f'./Yeast Resources/Pairwise/Spell/{folderName}/{model_specification}_specification.txt','w')
            f.write('Model Infromation\n')
            f.write(f'Hyperparameters\n\tlr: {lr}\n\tmomentum: {momentum}\n\tbatch: {batch}\n\n')
            f.write(f'Optimization\n\tOptimizer: SGD\n\tLoss Function: {lossFunc}\n')
            if lossFunc == 'FL' or lossFunc == 'WCE':
                f.write(f'\talpha: {alpha}\n')
            if lossFunc == 'FL':
                f.write(f'\tgamma: {gamma}\n')
            f.write(f'\nNetworks Information\n\tStructure: {struct}\n\tInput Dropout: {inputDropout}\n\tHidden Dropout: {hiddenDropout}\n')
            f.close()
        

        

    def trainNetwork(self,epochs,track=100,step_lr=5000,cyclicLr=False,partiallyTrained=False,parallel=False):
        #Initialize all pairs of training genes
        pairs = self.makePairs(self.training)
        testPairs = self.makePairs(self.validation)

        runningLoss = 0.0
        # If there already exists a lossList for this model and the network is not being reset, intialize the lost list from a file
        if(os.path.exists(self.lossLoc) and not(self.resetNet)):
            lossList = list(pd.read_csv(self.lossLoc).to_numpy().flatten())
        else:
            lossList = []

        if partiallyTrained:
            iterationRange = range(len(lossList*track),epochs)
        else:
            iterationRange = range(epochs)


        start = time.time()
        
        #Run training loop epochs number of times
        for iteration in iterationRange:
            #Reset gradients before running each training step
            self.opt.zero_grad()
            
            #Make batch array of gene pairs
            batchArray = self.makeBatchArray(pairs)
            
            #Make features and labels tensors from batcharray
            if parallel:
                features, labels = self.parallelMakeBatchTensor(batchArray)
            else:
                features, labels = self.makeBatchTensors(batchArray)
            
            #Move both tensors to device of model
            features = features.to(self.device)
            labels = labels.to(self.device)


            outputs = self.net(features.float())

            loss = self.lossFunc(outputs.float(),labels.float())
            runningLoss += loss.item()
            loss.backward()

            self.opt.step()
            if cyclicLr:
                self.scheduler.step()
            
            if iteration % track == 0:
                # If we are tracking the intial loss of the network, we need to scale to the loss as if it were the loss of a set of 'track' batches
                if iteration == 0:
                    runningLoss *= track
                
                # with torch.no_grad():
                #     testBatch = self.makeBatchArray(testPairs)
                #     testFeatures, testLabels = self.makeBatchTensors(testBatch)
                #     testFeatures = testFeatures.to(self.device)
                #     testLabels = testLabels.to(self.device)

                #     testOutput = self.net(testFeatures.float())

                #     testLoss = self.lossFunc(testOutput.float(),labels.float()).item() * track



                # lossList.append([iteration,runningLoss,testLoss,self.scheduler.get_last_lr()[0] if cyclicLr else self.lr])
                lossList.append([iteration,runningLoss])
                print(f'{track} Batch Cumulative Loss: {runningLoss}',flush=True)
                runningLoss = 0.0
                # pd.DataFrame(lossList,columns=['Batch','Training Loss','Testing Loss','Learning Rate']).to_csv(self.lossLoc,index=False)
                pd.DataFrame(lossList,columns=['Batch','Training Loss']).to_csv(self.lossLoc,index=False)
                
                print(f'Time for 100 Batches: {(time.time()-start)/60}',flush=True)
                start = time.time()
        torch.save(self.net.state_dict(),self.networkLoc)



    def testNetworkAll(self,proportionNeg=10,saveTerms={'GO:0007005','GO:0006302','GO:0007127'},runAll=True,validation=True):
        with torch.no_grad():
            #Helper function that passes a pair through the trained network, then grabs the outputs of that pair for a given GO term
            def calcPair(pair,termIndex):
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                outputsTensor = self.net(features.float(),test=True).cpu()
                outputs = np.array(outputsTensor,dtype='float32')
                labels = np.array(labels,dtype=np.intc)
                return([pair[0],pair[1],labels[0,termIndex],outputs[0,termIndex]])

            #Helper function that will take in a table of pairs, their label, and their scores, then calculate the confusion matrix statistics
            def calcStats(data):
                def calcMatrix(tp,tn,fp,fn):
                    accuracy = (tp+tn) / (tp+fn+fp+tn)
                    precision = 1 if (tp+fp) == 0 else tp / (tp+fp)
                    recall = 1 if (tp+fn) == 0 else tp / (tp+fn)
                    falsePositiveRate = fp / (fp+tn)
                    selectivity = tn / (tn+fp)
                    return [accuracy,precision,recall,falsePositiveRate,selectivity]
                
                #Sorts data by the third column, which is the pair confidence, in descending order
                sortedData = data[data[:,3].argsort()[::-1]]
                print(f'Sorted Data: {sortedData}')
                falseNeg = len([genePair for genePair in sortedData if genePair[2] == 1])
                truePos = 0
                trueNeg = len(sortedData) - falseNeg
                falsePos = 0
                

                #This loop calculates the the confusion matrix for all pairs in the table
                statistics =[]
                for genePair in sortedData:
                    if genePair[2] == 1:
                        truePos += 1
                        falseNeg -= 1
                    else:
                        trueNeg -= 1
                        falsePos += 1
                    statistics.append([truePos,falseNeg,trueNeg,falsePos] + calcMatrix(tp=truePos,tn=trueNeg,fp=falsePos,fn=falseNeg))
                
                return np.array(statistics,dtype='float32')
            
            #Helper function that calculates the convexed hulled average precision of the the entire table
            def averagePrecision(inputArray):
                precisionArray = np.copy(inputArray)
                for i in range(len(precisionArray)-1,0,-1):
                    if precisionArray[i] > precisionArray[i-1]:
                        precisionArray[i-1] = precisionArray[i]
                return np.mean(precisionArray)
            

            print("Began Testing the Network")
            allPairs = set([(pair[0],pair[1]) for pair in self.makePairs(self.validation if validation else self.training)])
            leafStatsDist = []
            columnNames = ['Gene A','Gene B','Label','Score','True Positive','False Negative','True Negative','False Positive','Accuracy','Precision','Recall','False Positive Rate','Selectivity']
            
            #Loops over all Go Slim terms
            for i in range(self.outputSize):
                if self.outputSize - 1 != i or (not(self.nonSpecific) and i == self.outputSize):
                    leaf = self.leaves[i]
                    print(f'Testing GO Term: {leaf[0]} ({i} / {self.outputSize})')
                    #Conditional determines whether a given GO term's performance is calculated
                    if leaf[0] in saveTerms or runAll:
                        #Positive genes are all genes in the validation set that are annotated to the GO term
                        posGenes = [gene for gene in self.validation if gene in leaf[1]]

                        #If no genes are annoated to the term in validation, make pair from all annotated genes
                        #This was put in termporarily to allow for the test function to run, but this is not a good way to test terms with no genes and should be replaced
                        if len(posGenes) == 0 or True:
                            posGenes = list(leaf[1])
                        posPairs = self.makePairs(np.array(posGenes))

                        #If there are more than 1000 positive pairs, shuffle the array and take the first 1000
                        if len(posPairs) > 1000:
                            np.random.shuffle(posPairs)
                            posPairs = posPairs[:1000]
                        
                        negPairs = np.array([[pair[0],pair[1]] for pair in allPairs - set([(pair[0],pair[1]) for pair in posPairs])])
                        np.random.shuffle(negPairs)
                        negPairs = negPairs[:len(posPairs)*proportionNeg]
                        testingPairs = np.concatenate([posPairs,negPairs])

                        # print(f'Pos Genes: {posGenes}')
                        # print(f'Pos piars: {posPairs}\nNeg Pairs: {negPairs}')

                        #Calculate the data for a term
                        termData = np.array([calcPair(pair,self.GOTermDict[leaf[0]]) for pair in testingPairs],dtype=object)
                        sortedData = termData[termData[:,3].argsort()[::-1]]
                        
                        stats = calcStats(termData)
                        termResults = np.concatenate([sortedData,stats],axis=1)
                        leafStatsDist.append([leaf[0],np.mean(termResults[:,10]),averagePrecision(termResults[:,9])])
                        goTerm = leaf[0].replace(':','-')
                        print('Are we attempting to save')
                        termDataFrame = pd.DataFrame(termResults,columns=columnNames)
                        termDataFrame.drop(termDataFrame.columns[[4,5,6,7,8,12]],axis=1,inplace=True)
                        termDataFrame.to_csv(f'{self.testLoc if validation else self.trainLoc}/{goTerm}_stats_fold{self.fold}.csv',index=False)
                else:
                    testingPairs = self.makeBatchArray(allPairs,batchSize=20000)

                    termData = np.array([calcPair(pair,self.outputSize-1) for pair in testingPairs],dtype=object)
                    sortedData = termData[termData[:,3].argsort()[::-1]]
                    
                    stats = calcStats(termData)
                    termResults = np.concatenate([sortedData,stats],axis=1)
                    leafStatsDist.append(['AnyCoAnno',np.mean(termResults[:,10]),averagePrecision(termResults[:,9])])
                    termDataFrame = pd.DataFrame(termResults,columns=columnNames)
                    termDataFrame.drop(termDataFrame.columns[[4,5,6,7,8,12]],axis=1,inplace=True)
                    termDataFrame.to_csv(f'{self.testLoc if validation else self.trainLoc}/AnyCoAnno_stats_fold{self.fold}.csv',index=False)
            if runAll:
                pd.DataFrame(leafStatsDist,columns=['GO Term','AUC','Average Precision']).to_csv(f'{self.testLoc if validation else self.trainLoc}/GOTermDistribution_fold{self.fold}.csv',index=False)
            


    #Makes input batches with pairs of genes, each pair being a list of two strings
    def makeBatchArray(self,pairs,batchSize=None):
        if batchSize == None:
            batchSize = self.batch
        #Returns array with batch size number of random gene pairs
        return pairs[np.random.choice(len(pairs),batchSize,replace=False),:]

    def makeBatchTensors(self,batchArray):
        # First, make an array of the features that are the pearson correlations between the gene pair in every gene expression dataset
        featuresList = []
        if self.expression:
            featuresList.append(torch.tensor([[self.calcCorr(dataset,genePair) for dataset in self.datasets] for genePair in batchArray],dtype=torch.float))
        if self.localization:
            featuresList.append(torch.tensor([[self.localizationScore(genePair,index) for index in range(23)] for genePair in batchArray],dtype=torch.float))
        if self.genomicInteraction:
            featuresList.append(torch.tensor([self.genomicScore(genePair) for genePair in batchArray],dtype=torch.float))
        if self.physical:
            featuresList.append(torch.tensor([self.physicalScore(genePair) for genePair in batchArray],dtype=torch.float))

        # Take array of features and convert it into a tensor
        features = torch.cat(featuresList,dim=1)

        # Create lists of labels
        labels = torch.tensor([[self.calcLabel(leaf,genePair) for leaf in self.leaves] for genePair in batchArray],dtype=torch.float)
        if self.nonSpecific:
            # print(torch.tensor([self.nonSpecificLabel(lab) for lab in labels]).size())
            # print(labels)
            labels = torch.cat([labels,torch.tensor([self.nonSpecificLabel(lab) for lab in labels])],dim=1)

        return (features,labels)

    def parallelMakeBatchTensor(self,batchArray):
        features = torch.zeros(size=(self.batch,self.inputSize),dtype=torch.float)
        labels = torch.zeros(size=(self.batch,self.outputSize),dtype=torch.float)
        

        def fillFeatures(start,finish):
            featuresList = []
            if self.expression:
                
                featuresList.append(torch.tensor([[self.calcCorr(dataset,genePair) for dataset in self.datasets] for genePair in batchArray[start:finish]],dtype=torch.float))
            if self.localization:
                featuresList.append(torch.tensor([[self.localizationScore(genePair,index) for index in range(23)] for genePair in batchArray[start:finish]],dtype=torch.float))
            if self.genomicInteraction:
                featuresList.append(torch.tensor([self.genomicScore(genePair) for genePair in batchArray[start:finish]],dtype=torch.float))
            if self.physical:
                featuresList.append(torch.tensor([self.physicalScore(genePair) for genePair in batchArray[start:finish]],dtype=torch.float))
            features[start:finish,:] = torch.cat(featuresList,dim=1)
            
        def fillLabels(start,finish):
            labels[start:finish,:] = torch.tensor([[self.calcLabel(leaf,genePair) for leaf in self.leaves] for genePair in batchArray[start:finish]],dtype=torch.float)
        
        def fillTensors(start,finish):
            fillFeatures(start,finish)
            fillLabels(start,finish)
        
        
        cpus = os.cpu_count()
        part = int(self.batch/cpus)

        threads = []
        for c in range(cpus):
            if c != cpus - 1:
                
                threads.append(threading.Thread(target=fillTensors,args=(part*c,part*(c+1))))
                threads[c].start()
            else:
                threads.append(threading.Thread(target=fillTensors,args=(part*c,self.batch)))
                threads[c].start()
        for c in range(cpus):
            threads[c].join()

        return(features,labels)
            


    
    #Helper function for makeBatchTensors - looks up and modifies correlation for a gene pair in a given dataset
    def calcCorr(self,d,gp):
        d = d.dataFile
        gene1 = gp[0]
        gene2 = gp[1]
        rho = self.corrDict.lookupCorrelation(gene1,gene2,d)

        #Adjust rho if 1 or -1 because of problems with fisher z transform
        if rho == 1:
            rho = 0.99
        elif rho == -1:
            rho = -0.99
        
        #Regularize Rho via fisher z transformation
        if self.regularize:
            mean, std = self.corrDict.expDataset.statsDict[d]
            regularizedRho = (np.arctanh(rho) -  mean) / std
            return regularizedRho
        else:
            return rho
        
    # Helper Function for makeBatchTensors - calcs label for a given GO Term
    def calcLabel(self,l,gpair):
            #If both genes are annotated to that GO term, return 1, otherwise, return 0
            if gpair[0] in l[1] and gpair[1] in l[1]:
                return 1
            else:
                return 0
            
    def nonSpecificLabel(self,vector):
        if torch.sum(vector).item() > 0:
            return [1]
        else:
            return [0]

    # Helper Function for makeBatchTensors - Predicate that is used to make the localization data section of the features tensor
    def localizationScore(self,gp,index):
        if gp[0] in self.localMap and gp[1] in self.localMap:
            if self.localMap[gp[0]][index] and self.localMap[gp[0]][index]:
                return 1
            else:
                return -1
        else:
            return 0

    # Helper Function for makeBatchTensor - returns list of what genetic interactions occur between gene pairs   
    def genomicScore(self,gp):
        genePairStr = gp[0] + ' ' + gp[1]
        if genePairStr in self.genomicMap:
            return self.genomicMap[genePairStr]
        else:
            return [0 for _ in range(6)]
        
    # Helper Function for makeBatchTensor - returns list of what physical interactions occur between gene pairs
    def physicalScore(self,gp):
        genePairStr = gp[0] + ' ' + gp[1]
        if genePairStr in self.physicalMap:
            return self.physicalMap[genePairStr]
        else:
            return [0 for _ in range(7)]
        
        
    #Returns array of all pairs of gene from given array of genes
    def makePairs(self,genes):
        arr = np.array([(genes[i],genes[j]) for i in range(len(genes)) for j in range(i+1,len(genes))],dtype='U10')
        return arr
    
    def makeNewGeneFolds(self,foldFile):
        #Take the union of all genes in the GO slim
        folds = []
        genes = set()
        for leaf in self.leaves:
            genes = genes | leaf[1]
        
        genes = list(genes)
        random.shuffle(genes)
        partition = int(len(genes) / self.numFolds)
        for  i in range(self.numFolds):
            for gene in genes[i*partition:(i+1)*partition]:
                folds.append([gene,i])
        pd.DataFrame(folds,columns=['Gene','Fold']).to_csv(foldFile,index=False)
        return folds

    def compareOverlap(self):
        pairs = self.makePairs(np.concatenate([self.training,self.validation],axis=0))
        leaves = getLeaves(10)
        totals = [0 for i in range(len(leaves))]
        for pair in pairs:
            for leaf in leaves:
                if pair[0] in leaf[1] and pair[1] in leaf[1]:
                    totals[self.GOTermDict[leaf[0]]] +=1
        for leaf in leaves:
            print(f'{leaf[0]} co-annotations: {totals[self.GOTermDict[leaf[0]]]}')
    
    def compareTermOverlap(self):
        start = time.time()
        leaves = getLeaves(10)
        mat = np.zeros(shape=(len(leaves),len(leaves)),dtype=float)
        allGenes = set(np.concatenate([self.training,self.validation],axis=0))
        for i,outLeaf in enumerate(leaves):
            for inLeaf in leaves:
                pvalue = 1 - stats.hypergeom.cdf(len(outLeaf[1] & inLeaf[1]),len(allGenes),len(inLeaf[1]),len(outLeaf[1]))
                mat[self.GOTermDict[outLeaf[0]],self.GOTermDict[inLeaf[0]]] = pvalue
            print(f'Calcualted {i+1}/{len(leaves)}term\nTime take: {(time.time()-start)/60} minutes')
        terms = ['' for i in range(len(self.GOTermDict))]
        for term, index in self.GOTermDict.items():
            terms[index] = term
        pd.DataFrame(mat,columns=terms).to_csv('./Yeast Resources/OverlapResults/Overlap.csv',index=False)
        


        
        


    
        







        







