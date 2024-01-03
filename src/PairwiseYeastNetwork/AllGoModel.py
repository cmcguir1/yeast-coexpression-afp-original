from random import random
from CorrelationDictionary import CorrelationDictionary
import pandas as pd
import numpy as np
from FlexNet import FlexNet
import torch
import time
import os
import random
from CustomLossFunctions import FocalLoss, CustomCrossEntropyLoss, SM_BCE, SM_MSE, ComboCrossEntropy
import threading
from torch.utils.data import Dataset

from scipy import stats


import sys
from YeastDataFile import YeastDataFile

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes


class AllGoModel():
    def __init__(self,fold,structure,folderName,modelName,numFolds=4,lr=0.01,min_lr=1e-7,momentum=0.9,batch=50,gamma=2,alpha=1,weightDecay=0.0,weighted=False,lossFunc='BCE',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold_Original_1.csv',ontologyDataset='modern',regularize=False,inputDropout=None,hiddenDropout=None,activation='relu',resetNet=False,cuda=True,inputVector = 'x',outputVector = 'b',verbose='',addTerms=[],memMapName='YeastDict_Regularized.npy',randomizeLabels=False,randomizeFeatures=False,swapGenes=False):
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
                    self.genomicMap[genePairStrA] = [0 for i in range(self.genomic_len)]
                    self.genomicMap[genePairStrB] = [0 for i in range(self.genomic_len)]
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
                interactions = pd.read_csv('../BIOGRID-ORGANISM-Saccharomyces_cerevisiae-2.0.25.tab.txt',sep="\t").to_numpy()
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
                    self.physicalMap[genePairStrA] = [0 for i in range(self.phys_len)]
                    self.physicalMap[genePairStrB] = [0 for i in range(self.phys_len)]
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
        
        self.leaves = getLeaves(10,dataset=ontologyDataset,bioProc=('b' in outputVector),molFunc=('m' in outputVector),cellComp=('c' in outputVector),exclude=['GO:0002181','GO:0022857','GO:0032543'])
        for term in addTerms:
            self.leaves.append([term,set(getGenes(term,dataset=ontologyDataset))])
        self.GOTermDict = {term[0]: i for i,term in enumerate(self.leaves)}
        self.outputSize = len(self.leaves)
        
        self.nonSpecific = 'n' in outputVector
        if self.nonSpecific:
            self.outputSize += 1

        self.unrelated= 'u' in outputVector
        if self.unrelated:
            self.outputSize += 1
        
        
        
        
        if foldFile or 'original' or foldFile == 'Original' or foldFile == '2009':
            foldFile = './src/PairwiseYeastNetwork/AllGOGeneFold_Original_1.csv'
        elif foldFile == 'modern' or foldFile == 'Modern' or foldFile == '2023':
            foldFile = './src/PairwiseYeastNetwork/AllGOGeneFold1.csv'


        # If the foldFile does not exit, make new gene folds; Otherwise, generate val and training data from the foldFile
        print(foldFile)
        if not os.path.exists(foldFile):
            folds = self.makeNewGeneFolds(foldFile=foldFile)
            print('Making new folds file')
        else:
            #Read in file of gene folds
            folds = pd.read_csv(foldFile).to_numpy()


        
        
        self.validation = np.array([gene[0] for gene in folds if gene[1] == fold],dtype='U10')
        
        self.training = np.array([gene[0] for gene in folds if gene[1] != fold],dtype='U10')
        print(f'Intersection: {len(set(self.training) & set(self.validation))}')
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

        lr_name = '' if lr == 0.001 and not('l' in verbose) else f'_lr{lr}'
        batch_name = '' if batch == 500 and not('b' in verbose) else f'_batch{batch}'
        weightDecay_Name = '' if weightDecay == 0.0  and not('w' in verbose)else f'_wd{weightDecay}'
        lf_name = '' if lossFunc == 'CE' and not('f' in verbose) else f'_lf{lossFunc}'
        momentum_name = '' if momentum == 0.9 and not('m' in verbose) else f'_momentum{momentum}'
        alpha_name = '' if alpha == 1 and not('a' in verbose) else f'_alpha{alpha}'
        gamma_name = '' if gamma == 2 and not('g' in verbose) else f'_gamma{gamma}'

        input_name = ''.join(sorted(inputVector))
        output_name = ''.join(sorted(outputVector))

        struct = f'{self.inputSize}x{structure}x{self.outputSize}'

        model_specification = f'{modelName}_{input_name}_{output_name}_{struct}{lr_name}{batch_name}{weightDecay_Name}{lf_name}{momentum_name}{alpha_name}{gamma_name}{inputDrop_name}{hiddenDrop_name}'

        
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
            print(f'Loaded Network from Hard drive')
        
        #Choose which device to run network on, then move network to that device
        self.device = 'cuda:0' if torch.cuda.is_available() and cuda else 'cpu'
        self.net.to(self.device)
        print('Initialized Network')

        if weighted:
            # Formula for the weight of each GO term is (N^2/n^2) where:
            #   N - the total number of genes across all fold
            #   n - the number of gene annotated to a given go term
            # Weights are then divided by the sum of weights so that they add to zero, then they are multiplied by the number of output nodes
            self.weights = torch.tensor([pow(len(folds),2) / pow(len(leaf[1]),2) for leaf in self.leaves],dtype=torch.float)**alpha
            self.weights = (self.weights / torch.sum(self.weights)) * len(self.leaves)

        else:
            self.weights = torch.ones((self.outputSize,),dtype=float)
        
        self.weights = self.weights.to(self.device)
        

        #Initialize Loss function, we are using CEL because we have multiple outputs that could be true
        if lossFunc in ['CE','crossEntropy','cross_entropy']:
            # self.lossFunc = torch.nn.CrossEntropyLoss()
            self.lossFunc = CustomCrossEntropyLoss(alpha=self.weights,nonSpecific='n' in outputVector)
            self.trainNegatives = 'n' in outputVector

            print('Used Cross Entropy Loss Function')
        elif lossFunc in ['FL','focalLoss','focal_loss']:
            self.lossFunc = FocalLoss(gamma=gamma,alpha=self.weights,nonSpecific='n' in outputVector)
        elif lossFunc in ['WCE']:
            self.lossFunc = torch.nn.CrossEntropyLoss(weight=self.weights)
        elif lossFunc in ['BCE','binaryCrossEntropy','binary_cross_entropy']:
            self.lossFunc = torch.nn.BCEWithLogitsLoss(weight=self.weights)
            self.trainNegatives = True
        elif lossFunc in ['SF_MSE']:
            self.lossFunc = SM_MSE()
        elif lossFunc in ['MSE']:
            self.lossFunc = torch.nn.MSELoss()
        elif lossFunc in ['SM_BCE']:
            self.lossFunc = SM_BCE()
            self.trainNegatives = True
        elif lossFunc in ['CCE']:
            self.lossFunc = ComboCrossEntropy()
        else:
            self.lossFunc = torch.nn.CrossEntropyLoss()
            # self.lossFunc = CustomCrossEntropyLoss(alpha=self.weights,nonSpecific='n' in outputVector)
            print('Used Cross Entropy Loss Function')
        
        
        #Stochastic Gradient Descent Optimizer
        self.opt = torch.optim.SGD(self.net.parameters(),lr=lr,momentum=momentum,weight_decay=weightDecay)
        # self.scheduler = torch.optim.lr_scheduler.CyclicLR(self.opt,base_lr=min_lr,max_lr=lr,step_size_up=10000,step_size_down=10000)

        
        # This section of code sets up dictionaries connecting random gene pairs that can be used for random controls
        self.geneSwap = {}
        self.geneSwapReverse = {}
        randomFolds = np.random.RandomState(seed=42).permutation(folds)
        for gene, randomGene in zip(folds,randomFolds):
            self.geneSwap[gene[0]] = randomGene[0]
            self.geneSwapReverse[randomGene[0]] = gene[0]
    
        self.randomizeLabels = randomizeLabels
        self.randomizeFeatures = randomizeFeatures
        self.swapGenes = swapGenes


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

        # This section saves the information about a network's hyperparameters, loss function, and network structure to a text file
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
        

        

    def trainNetwork(self,epochs,track=100,printTensors=False,numTest=10):
        self.net.train()

        # If swapping genes, train by swapping labels and using normal features
        if self.swapGenes:
            self.randomizeLabels = True
            self.randomizeFeatures = False

        
        # Pairs that will be sampled from during training
        posPairs, negPairs = self.makePosNegPairs(self.training)
        testPairs, negTest = self.makePosNegPairs(self.validation)
        
        

        runningLoss = 0.0
        # If there already exists a lossList for this model and the network is not being reset, intialize the lost list from a file
        if(os.path.exists(self.lossLoc) and not(self.resetNet)):
            lossList = pd.read_csv(self.lossLoc).values.tolist()
            print(f'Loss List:\n{lossList}')
        else:
            lossList = []

        
    
        if len(lossList) > 0:
            iterRange = range(int(lossList[len(lossList)-1][0])+track,int(lossList[len(lossList)-1][0]+track+epochs))
        else:
            iterRange = range(epochs)

        start = time.time()
        #Run training loop epochs number of times
        for iteration in iterRange:
            #Reset gradients before running each training step
            self.net.train()
            self.opt.zero_grad()
            
            # Create features and labels for a batch
            if self.trainNegatives:
                batchArray = self.makeBatchArrayPartitioned(posPairs=posPairs,negPairs=negPairs)
            else:
                batchArray = self.makeBatchArray(posPairs)
            features, labels = self.makeBatchTensors(batchArray)
            
            
            # Move both tensors to device of model
            features = features.to(self.device)
            labels = labels.to(self.device)
            
            # Feed features through network to produce outputs
            outputs = self.net(features.float())
            
            # use outputs and labels to calculate loss for batch
            loss = self.lossFunc(outputs.float(),labels.float())
            

            
            runningLoss += loss.item()
            
            # Backpropagate
            loss.backward()

            self.opt.step()
    

            if printTensors:
                print(f'Batch Array: {batchArray}')
                print(f'Features: {features}')
                print(f'Labels: {torch.sum(labels)}')
                print(f'Outputs: {outputs}')
                print(f'Loss: {loss}\n')
            
            if iteration % track == 0:
                # If we are tracking the intial loss of the network, we need to scale to the loss as if it were the loss of a set of 'track' batches
                if iteration == 0:
                    runningLoss *= track
                
                # Evaluate the network's loss for numTest number of validation examples
                self.net.eval()
                with torch.no_grad():
                    testLoss = 0
                    for i in range(numTest):
                        if self.trainNegatives:
                            testBatch = self.makeBatchArrayPartitioned(testPairs,negTest)
                        else:
                            testBatch = self.makeBatchArray(testPairs)
                        testFeatures, testLabels = self.makeBatchTensors(testBatch)
                        testFeatures = testFeatures.to(self.device)
                        testLabels = testLabels.to(self.device)

                        testOutput = self.net(testFeatures.float())

                        testLoss += self.lossFunc(testOutput.float(),labels.float()).item()
                    testLoss *= track / numTest

                
                lossList.append([iteration,runningLoss,testLoss])
                print(f'{track} Batch Cumulative Loss: {runningLoss}',flush=True)
                runningLoss = 0.0
                pd.DataFrame(lossList,columns=['Batch','Training Loss','Validation Loss']).to_csv(self.lossLoc,index=False)
                print(f'Time for 100 Batches: {(time.time()-start)/60}',flush=True)
                start = time.time()
        torch.save(self.net.state_dict(),self.networkLoc)



    def testNetworkAll(self,proportionNeg=10,saveTerms={'GO:0007005','GO:0006302','GO:0007127'},runAll=True,validation=True):
        self.net.eval()
        if self.swapGenes:
            self.randomizeLabels = False
            self.randomizeFeatures = True
        
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
            allPairs = [(pair[0],pair[1]) for pair in self.makePairs(self.validation if validation else self.training)]
            leafStatsDist = []
            columnNames = ['Gene A','Gene B','Label','Score','True Positive','False Negative','True Negative','False Positive','Accuracy','Precision','Recall','False Positive Rate','Selectivity']
            
            #Loops over all Go Slim terms
            for i in range(self.outputSize - (1 if self.nonSpecific or self.unrelated else 0)):
                # if self.outputSize - 1 != i and (not(self.nonSpecific)):
                leaf = self.leaves[i]
                print(f'Testing GO Term: {leaf[0]} ({i} / {self.outputSize})')
                #Conditional determines whether a given GO term's performance is calculated
                if leaf[0] in saveTerms or runAll:
                    #Positive genes are all genes in the validation set that are annotated to the GO term
                    posGenes = [gene for gene in (self.validation if validation else self.training) if gene in leaf[1]]
                    
                    posPairs = self.makePairs(np.array(posGenes))
                    if len(posPairs) > 0:

                        #If there are more than 1000 positive pairs, shuffle the array and take the first 1000
                        if len(posPairs) > 1000:
                            np.random.shuffle(posPairs)
                            posPairs = posPairs[:1000]
                        
                        negGenes = [gene for gene in (self.validation if validation else self.training) if not(gene in leaf[1])]
                        negPairs = self.makePairs(np.array(negGenes))
                        # negPairs = np.array([[pair[0],pair[1]] for pair in set(allPairs) - set([(pair[0],pair[1]) for pair in posPairs])])
                        np.random.shuffle(negPairs)
                        negPairs = negPairs[:len(posPairs)*proportionNeg]
                        testingPairs = np.concatenate([posPairs,negPairs])

                        

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
            if self.nonSpecific:  
                testingPairs = self.makeBatchArray(self.makePairs(self.validation if validation else self.training),batchSize=20000)

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
    
    def makeBatchArrayPartitioned(self,posPairs,negPairs,batchSize=None):
        if batchSize == None:
            batchSize = self.batch
        posBatch = posPairs[np.random.choice(len(posPairs),int(batchSize/2),replace=False),:]
        negBatch = negPairs[np.random.choice(len(negPairs),int(batchSize/2),replace=False),:]
        return np.concatenate([posBatch,negBatch],axis=1)

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
        if self.nonSpecific or self.unrelated:
            labels = torch.cat([labels,torch.tensor([self.nonSpecificLabel(lab) for lab in labels])],dim=1)

        return (features,labels)


    
    #Helper function for makeBatchTensors - looks up and modifies correlation for a gene pair in a given dataset
    def calcCorr(self,d,gp):
        d = d.dataFile
        if self.randomizeFeatures:
            gene1 = self.geneSwapReverse[gp[0]]
            gene2 = self.geneSwapReverse[gp[1]]
        else:
            gene1 = gp[0]
            gene2 = gp[1]
        rho = self.corrDict.lookupCorrelation(gene1,gene2,d)
        return rho
        
    # Helper Function for makeBatchTensors - calcs label for a given GO Term
    def calcLabel(self,l,gpair):
        if self.randomizeLabels:
            if self.geneSwap[gpair[0]] in l[1] and self.geneSwap[gpair[1]] in l[1]:
                return 1
            else:
                return 0
        else:
            #If both genes are annotated to that GO term, return 1, otherwise, return 0
            if gpair[0] in l[1] and gpair[1] in l[1]:
                return 1
            else:
                return 0
            
    def nonSpecificLabel(self,vector):
        if self.unrelated:
            if torch.sum(vector).item() == 0:
                return [1]
            else:
                return [0]
        else:
            if torch.sum(vector).item() > 0:
                return [1]
            else:
                return [0]

    # Helper Function for makeBatchTensors - Predicate that is used to make the localization data section of the features tensor
    def localizationScore(self,gp,index):
        if self.randomizeFeatures:
            gp[0] = self.geneSwapReverse[gp[0]]
            gp[1] = self.geneSwapReverse[gp[1]]
        if gp[0] in self.localMap and gp[1] in self.localMap:
            if self.localMap[gp[0]][index] and self.localMap[gp[0]][index]:
                return 1
            else:
                return -1
        else:
            return 0

    # Helper Function for makeBatchTensor - returns list of what genetic interactions occur between gene pairs   
    def genomicScore(self,gp):
        if self.randomizeFeatures:
            gp[0] = self.geneSwapReverse[gp[0]]
            gp[1] = self.geneSwapReverse[gp[1]]
        genePairStr = gp[0] + ' ' + gp[1]
        if genePairStr in self.genomicMap:
            return self.genomicMap[genePairStr]
        else:
            return [0 for _ in range(self.genomic_len)]
        
    # Helper Function for makeBatchTensor - returns list of what physical interactions occur between gene pairs
    def physicalScore(self,gp):
        if self.randomizeFeatures:
            gp[0] = self.geneSwapReverse[gp[0]]
            gp[1] = self.geneSwapReverse[gp[1]]
        genePairStr = gp[0] + ' ' + gp[1]
        if genePairStr in self.physicalMap:
            return self.physicalMap[genePairStr]
        else:
            return [0 for _ in range(self.phys_len)]
        
        
    #Returns array of all pairs of gene from given array of genes
    def makePairs(self,genes):
        arr = np.array([(genes[i],genes[j]) for i in range(len(genes)) for j in range(i+1,len(genes))],dtype='U10')
        return arr
    
    # Returns tuple of array of positive pairs (gene pairs with at least one coAnnotation), and negative pairs (gene pair with no coAnnotations)
    def makePosNegPairs(self,genes):
        posPairs = []
        negPairs = []
        for i in range(len(genes)):
            for j in range(i+1,len(genes)):
                if self.coAnnotated(genes[i],genes[j]):
                    posPairs.append([genes[i],genes[j]])
                else:
                    negPairs.append([genes[i],genes[j]])
        return (np.array(posPairs,dtype='U10'),np.array(negPairs,dtype='U10'))

    def coAnnotated(self,geneA,geneB):
        for leaf in self.leaves:
            if geneA in leaf[1] and geneB in leaf[1]:
                return True
        return False

    
    def makeNewGeneFolds(self,foldFile):
        #Take the union of all genes in the GO slim
        folds = []
        genes = set()
        for leaf in self.leaves:
            genes = genes | leaf[1]
        
        genes = list(genes)
        random.shuffle(genes)
        partition = int(len(genes) / self.numFolds)
        for i in range(self.numFolds):
            if i == self.numFolds - 1:
                for gene in genes[i*partition:]:
                    folds.append([gene,i])
            else: 
                for gene in genes[i*partition:(i+1)*partition]:
                    folds.append([gene,i])
        pd.DataFrame(folds,columns=['Gene','Fold']).to_csv(foldFile,index=False)
        return folds
    
    class CustomDataset(Dataset):
        def __init__(self,outerClass,pairs):
            self.out = outerClass
            self.pairs = pairs

        def __len__(self):
            return len(self.pairs)

        def __getitem__(self):
            batchArray = self.out.makeBatchArray(self.pairs)
            features, labels = self.out.makeBatchTensors(batchArray)
            return (features, labels)
            

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

    
        


        
        


    
        







        







