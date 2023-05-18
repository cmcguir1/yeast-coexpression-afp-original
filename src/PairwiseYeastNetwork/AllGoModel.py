from dataclasses import dataclass
from random import random
from CorrelationDictionary import CorrelationDictionary
from site import makepath
import pandas as pd
import numpy as np
from FlexNet import FlexNet
from ExpressionDatasets import ExpressionDatasets
import torch
import time
import os
from ConfusionMatrix import ConfusionMatrix
import random
from FocalLoss import FocalLoss

from scipy import stats


import sys
from YeastDataFile import YeastDataFile

sys.path.insert(0,'./obopy')
from Leaf import getLeaves


class AllGoModel():
    def __init__(self,fold,structure,folderName,modelName,numFolds=4,lr=0.01,momentum=0.9,batch=50,gamma=2,alpha=1,weighted=True,step=1000,stepGamma=0.95,decay_lr=False,lossFunc='CE',softmax=False,foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',ontologyDataset='modern',regularize=True, inputDropout=None,hiddenDropout=None,activation='relu',resetNet=False,inMemory=False,cuda=True,onlyBioProc=False):
        #getLeaves returns a list of tuple of (GO Term,{set of genes})
        if onlyBioProc:
            self.leaves = getLeaves(10,dataset=ontologyDataset,molFunc=False,cellComp=False)
            GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary_BioProcOnly.csv').to_numpy()
        else:
            self.leaves = getLeaves(10,dataset=ontologyDataset)
            GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()

        # pd.DataFrame([[leaf[0],i] for i, leaf in enumerate(self.leaves)],columns=['GO Term','Index']).to_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv',index=False)
        
        self.GOTermDict = {term[0]: term[1] for term in GoTerms}

        
        #Lists that will store the training and validation data
        val = []
        train = []
        folds = []
        if foldFile or 'original' or foldFile ==  'Original' or foldFile == '2009':
            foldFile = './src/PairwiseYeastNetwork/AllGOGeneFold_Orignial_1.csv'
        elif foldFile == 'modern' or foldFile == 'Modern' or foldFile == '2023':
            foldFile = './src/PairwiseYeastNetwork/AllGOGeneFold1.csv'
        #Checks if a folds file already exists, if not, make it
        if not os.path.exists(foldFile):
            #Take the union of all genes in the GO slim
            genes = set()
            for leaf in self.leaves:
                genes = genes | leaf[1]
            
            genes = list(genes)
            random.shuffle(genes)
            partition = int(len(genes) / numFolds)
            for  i in range(numFolds):
                for gene in genes[i*partition:(i+1)*partition]:
                    folds.append([gene,i])
            pd.DataFrame(folds,columns=['Gene','Fold']).to_csv(foldFile,index=False)
        #Otherwise, generate val and training data from the fold list
        else:
            #Read in file of gene folds
            folds = pd.read_csv(foldFile).to_numpy()

        self.folds = folds

        #Loop over all genes in folds
        for gene in folds:
            #If gene's fold matches fold variable, add to validation list
            if gene[1] == fold:
                val.append(gene[0])
            #Otherwise, add ot training list
            else:
                train.append(gene[0])
    
        #Make instance varaibles of array of training genes and array of validation genes
        self.training = np.array(train)
        np.random.shuffle(self.training)
        
        self.validation = np.array(val)

        print('Initialized training and validation data')


        
        #Correlations Dictionary that will be retrieve precalculated correlation values
        self.corrDict = CorrelationDictionary(dictLoc='../YeastMemMap/YeastCorrDictionary.dat' if (os.path.exists('../YeastMemMap/YeastCorrDictionary.dat')) else '../YeastDict.dat',datasetType=ontologyDataset,inMemory=inMemory)
        self.datasets = self.corrDict.expDataset.datasets
        
        #Initialize all expression data as a list of maps {gene -> expression array}
        # self.datasets = ExpressionDatasets('./Yeast Resources/Datasets/All Spell/all spell datasets',recur=True,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv').datasets

        inputDropString = '' if inputDropout == None or inputDropout == 0 else f'_inputDrop{inputDropout}'
        hiddenDropString = '' if hiddenDropout == None or hiddenDropout == 0 else f'_hiddenDrop{hiddenDropout}'

        #Instance variable for batch size
        self.batch = batch
        self.fold = fold
        self.regularize = regularize

        print('Initialized Expression Datasets')

        struct = f'{len(self.datasets)}x{structure}x{len(self.leaves)}'
        print(struct)
        #Initialize the network, the size of the input layer is the number of expression datasets, and the size of the output is the number of leaf go terms
        self.networkLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}{inputDropString}{hiddenDropString}_Net_fold{self.fold+1}.pth'
        
        if inputDropout == 0:
            inputDropout = None
        if hiddenDropout == 0:
            hiddenDropout = None

        self.resetNet = resetNet
        self.softmax = softmax
        self.sm = torch.nn.Softmax(dim=1)

        self.net = FlexNet(struct,sigmoid=False,activation=activation,inputDrop=inputDropout,hiddenDrop=hiddenDropout)
        if(os.path.exists(self.networkLoc) and  not(resetNet)):
            self.net.load_state_dict(torch.load(self.networkLoc))
        print('Initialized Network')
        #Choose which device to run network on, then move network to that device
        self.device = 'cuda:0' if torch.cuda.is_available() and cuda else 'cpu'
        self.net.to(self.device)

        # Know that this conditional is currently being blocked
        if weighted and False:
            alphaValues = pd.read_csv('./src/PairwiseYeastNetwork/AllGOAlphaDictionary.csv').to_numpy()
            self.weights=torch.zeros((92,),dtype=torch.float32)
            for val in alphaValues:
                self.weights[self.GOTermDict[val[0]]] = val[1]
            self.weights = self.weights**alpha
            self.weights = (self.weights / torch.sum(self.weights)) * 92.0
            #self.weights = torch.ones(size=(92,))
            print(self.weights)
        else:
            self.weights = torch.ones((92,),dtype=float)
        
        self.weights = self.weights.to(self.device)
        

        #Initialize Loss function, we are using CEL because we have multiple outputs that could be true
        if lossFunc in ['CE','crossEntropy','cross_entropy']:
            self.lossFunc = torch.nn.CrossEntropyLoss()
            print('Used Cross Entropy Loss Function')
        elif lossFunc in ['WCE','weightedCrossEntropy','weighted_cross_entropy']:
            self.lossFunc = torch.nn.CrossEntropyLoss(weight=self.weights)
            print('Used Weighted Cross Entropy Loss Function')
        elif lossFunc in ['FL','focalLoss','focal_loss']:
            self.lossFunc = FocalLoss(gamma,alpha=alpha)
            #self.softmax = True
        else:
            self.lossFunc = torch.nn.CrossEntropyLoss()
            print('Used Cross Entropy Loss Function')
        
        #Stochastic Gradient Descent Optimizer
        self.opt = torch.optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)
        #self.scheduler = torch.optim.lr_scheduler.StepLR(self.opt,step_size=step,gamma=stepGamma)
        lamb = lambda epoch: 0.95**epoch
        self.scheduler = torch.optim.lr_scheduler.LambdaLR(self.opt,lr_lambda=lamb)
        self.decay_lr = decay_lr

        

        #Locations to save all output data
        
        self.lossLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}{inputDropString}{hiddenDropString}_Loss_fold{self.fold+1}.csv'
        #The locations for the testing and training data will be folder because they will be storing a csv file for each GO term
        self.trainLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}{inputDropString}{hiddenDropString}_Train_/'
        self.testLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}{inputDropString}{hiddenDropString}_Test_/'
        print(self.trainLoc)
        print(self.testLoc)

        #These three conditional check if the folder that the output data will be stored exist, and if not, construct those folders
        if not os.path.exists(f'./Yeast Resources/Pairwise/Spell/{folderName}'):
            os.mkdir(f'./Yeast Resources/Pairwise/Spell/{folderName}')
        
        if not os.path.exists(self.testLoc):
            os.mkdir(self.testLoc)

        if not os.path.exists(self.trainLoc):
            os.mkdir(self.trainLoc)

        

    def trainNetwork(self,epochs,sigmoid=False,track=100,step_lr=5000):
        #Initialize all pairs of training genes
        pairs = self.makePairs(self.training)
        # print(f'Pairs: {pairs}')

        runningLoss = 0.0
        if(os.path.exists(self.lossLoc) and not(self.resetNet)):
            lossList = list(pd.read_csv(self.lossLoc).to_numpy().flatten())
            #print(f'Intial Loss List: {lossList}')
        else:
            lossList = []

        

        start = time.time()
        #Run training loop epochs number of times
        for epoch in range(epochs):
            #Reset gradients before running each training step
            self.opt.zero_grad()
            
            #Make batch array of gene pairs
            batchArray = self.makeBatchArray(pairs)
            #Make features and labels tensors from batcharray
            features, labels = self.makeBatchTensors(batchArray)
            #Move both tensors to device of model
            features = features.to(self.device)
            labels = labels.to(self.device)


            outputs = self.net(features.float())
            if self.softmax:
                outputs = self.sm(outputs)

            loss = self.lossFunc(outputs.float(),labels.float())
            runningLoss += loss.item()
            loss.backward()
            #print(f'Time Feed forward and calculate loss: {(time.time()-begin)/60}')
            self.opt.step()
            if epoch % (step_lr) == 0 and epoch != 0:
                self.scheduler.step()
            
            if epoch % track == 0:
                if epoch == 0:
                    runningLoss *= track
                lossList.append(runningLoss)
                print(f'{track} Batch Cumulative Loss: {runningLoss}')
                runningLoss = 0.0
                pd.DataFrame(lossList,columns=['Loss']).to_csv(self.lossLoc,index=False)
                print(f'Time for 100 Batches: {(time.time()-start)/60}\n---------------------')
                start = time.time()
        torch.save(self.net.state_dict(),self.networkLoc)
        #self.net._save_to_state_dict(self.networkLoc)


    def testNetworkAll(self,proportionNeg=10,saveTerms={'GO:0007005','GO:0006302','GO:0007127'},runAll=True,validation=True):
        with torch.no_grad():
            #Helper function that passes a pair through the trained network, then grabs the outputs of that pair for a given GO term
            def calcPair(pair,termIndex):
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                outputsTensor = self.net(features.float(),test=True).cpu()
                if self.softmax:
                    outputsTensor = self.sm(outputsTensor)
                outputs = np.array(outputsTensor,dtype='float32')
                labels = np.array(labels,dtype=np.intc)
                # print(f'Shape of Labels: {labels.shape}')
                # print(f'Shape of Outputs: {outputs.shape}')
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
            for i, leaf in enumerate(self.leaves):
                print(f'Testing GO Term: {leaf[0]} ({i} / {len(self.leaves)})')
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
            if runAll:
                pd.DataFrame(leafStatsDist,columns=['GO Term','AUC','Average Precision']).to_csv(f'{self.testLoc if validation else self.trainLoc}/GOTermDistribution_fold{self.fold}.csv',index=False)
            


    #Makes input batches with pairs of genes, each pair being a list of two strings
    def makeBatchArray(self,pairs):
        #Returns array with batch size number of random gene pairs
        return pairs[np.random.choice(len(pairs),self.batch,replace=False),:]

    def makeBatchTensors(self,batchArray):
        #Helper function for calculating correlations in list comprehension
        def calcCorr(d,gp):
            d = d.dataFile
            gene1 = gp[0]
            gene2 = gp[1]
            rho = self.corrDict.lookupCorrelation(gene1,gene2,d)
            # print(f'rho from pre-calculated coefficients: {rho}')

            # rho = d.customCorrelation(gp)

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
        
        def calcLabel(l,gpair):
            #If both genes are annotated to that GO term, return 1, otherwise, return 0
            if gpair[0] in l[1] and gpair[1] in l[1]:
                return 1
            else:
                return 0

        features = torch.tensor([[calcCorr(dataset,genePair) for dataset in self.datasets] for genePair in batchArray],dtype=float)
        labels = torch.tensor([[calcLabel(leaf,genePair) for leaf in self.leaves] for genePair in batchArray],dtype=float)
        #labels = torch.zeros((len(batchArray),len(self.leaves)),dtype=float)
        for i in range(len(batchArray)):
            for leaf in self.leaves:
                if batchArray[i,0] in leaf[1] and batchArray[i,1] in leaf[1]:
                    labels[i,self.GOTermDict[leaf[0]]] = 1.0

        if self.softmax:
            labels = self.sm(labels)
        return (features,labels)
        
    #Returns array of all pairs of gene from given array of genes
    def makePairs(self,genes):
        pairs = []
        #Loop over all genes
        
        arr = np.array([(genes[i],genes[j]) for i in range(len(genes)) for j in range(i+1,len(genes))])
        return arr

    def testTrainingPollution(self):
        trainSet = set(self.training)
        testSet = set(self.validation)
        print(f'Length testing: {len(testSet)}\nLength training: {len(trainSet)}')
        print(f'Intersection of train and test: {len(trainSet & testSet)}')
        trainPairs = set(list(self.makePairs(self.training)))
        testPairs = set(list(self.makePairs(self.validation)))
        print(f'Length testing pairs: {len(testPairs)}\nLength training pairs: {len(trainPairs)}')
        print(f'Intersection of train and test: {len(trainPairs & testPairs)}')

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
        

        
        


    
        







        







