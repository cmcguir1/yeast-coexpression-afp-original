from dataclasses import dataclass
from CorrelationDictionary import CorrelationDictionary
from site import makepath
import statistics
import pandas as pd
import numpy as np
from FlexNet import FlexNet
from ExpressionDatasets import ExpressionDatasets
import torch
import time
import threading
import concurrent.futures
import os

#import for cython
import cython



import sys
from YeastDataFile import YeastDataFile

sys.path.insert(0,'./obopy')
from Leaf import getLeaves


class AllGoModel():
    def __init__(self,fold,structure,folderName,modelName,numFolds=4,lr=0.01,momentum=0.9,batch=50,foldFile='',ontologyDataset='modern',regularize=True,memMapLoc='../YeastDict.dat'):
        #getLeaves returns a list of tuple of (GO Term,{set of genes})
        self.leaves = getLeaves(10,dataset=ontologyDataset)

        # pd.DataFrame([[leaf[0],i] for i, leaf in enumerate(self.leaves)],columns=['GO Term','Index']).to_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv',index=False)
        GoTerms = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
        self.GOTermDict = {term[0]: term[1] for term in GoTerms}

        #Lists that will store the training and validation data
        val = []
        train = []
        folds = []
        #Checks if a folds file was given, if not, make a new fold of genes from the GO slim
        if foldFile == '':
            #Take the union of all genes in the GO slim
            genes = set()
            for leaf in self.leaves:
                genes = genes | leaf[1]
            
            genes = list(genes)
            partition = int(len(genes) / numFolds)
            for  i in range(numFolds):
                for gene in genes[i*partition:(i+1)*partition]:
                    folds.append([gene,i])
        #Otherwise, generate val and training data from the fold list
        else:
            #Read in file of gene folds
            folds = pd.read_csv(foldFile).to_numpy()

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
        
        self.validation = np.array(val)

        print('Initialized training and validation data')


        
        #Correlations Dictionary that will be retrieve precalculated correlation values
        self.corrDict = CorrelationDictionary(dictLoc=memMapLoc)
        self.datasets = self.corrDict.datasets
        
        #Initialize all expression data as a list of maps {gene -> expression array}
        # self.datasets = ExpressionDatasets('./Yeast Resources/Datasets/All Spell/all spell datasets',recur=True,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv').datasets

      

        print('Initialized Expression Datasets')


        #Initialize the network, the size of the input layer is the number of expression datasets, and the size of the output is the number of leaf go terms
        struct = f'{len(self.datasets)}x{structure}x{len(self.leaves)}'
        self.net = FlexNet(struct,sigmoid=False)
        print('Initialized Network')
        #Choose which device to run network on, then move network to that device
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)


        #Initialize Loss function, we are using CEL because we have multiple outputs that could be true
        self.lossFunc = torch.nn.CrossEntropyLoss()
        #Stochastic Gradient Descent Optimizer
        self.opt = torch.optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)
        #Instance variable for batch size
        self.batch = batch
        self.fold = fold
        self.regularize = regularize

        #Locations to save all output data
        self.networkLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}_Net_fold{self.fold+1}.csv'
        self.lossLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}_Loss_fold{self.fold+1}.csv'
        #The locations for the testing and training data will be folder because they will be storing a csv file for each GO term
        self.trainLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}_Train_/'
        self.testLoc = f'./Yeast Resources/Pairwise/Spell/{folderName}/{modelName}_{struct}_Test_/'

        #These three conditional check if the folder that the output data will be stored exist, and if not, construct those folders
        if not os.path.exists(f'./Yeast Resources/Pairwise/Spell/{folderName}'):
            os.mkdir(f'./Yeast Resources/Pairwise/Spell/{folderName}')
        
        if not os.path.exists(self.testLoc):
            os.mkdir(self.testLoc)

        if not os.path.exists(self.trainLoc):
            os.mkdir(self.trainLoc)

        

    def trainNetwork(self,epochs):
        #Initialize all pairs of training genes
        pairs = self.makePairs(self.training)
        # print(f'Pairs: {pairs}')

        runningLoss = 0.0
        lossList = []
        start = time.time()
        #Run training loop epochs number of times
        for epoch in range(epochs):
            #Reset gradients before running each training step
            self.opt.zero_grad()
            begin = time.time()
            
            #Make batch array of gene pairs
            batchArray = self.makeBatchArray(pairs)
            # print(f'Batch Array: {batchArray}')
            # print(f'Batch Array:\n{batchArray}')
            #Make features and labels tensors from batcharray
            features, labels = self.makeBatchTensors(batchArray)
            #print(f'Time to calculate correlations and create batches: {(time.time()-begin)/60}')
            begin = time.time()
            # print(f'Features:\n{features}')
            # print(f'Labels:\n{labels}')
            #Move both tensors to device of model
            features = features.to(self.device)
            labels = labels.to(self.device)

            outputs = self.net(features.float())
            loss = self.lossFunc(outputs.float(),labels.float())
            runningLoss += loss.item()
            loss.backward()
            #print(f'Time Feed forward and calculate loss: {(time.time()-begin)/60}')
            self.opt.step()
            
            if epoch % 100 == 0 and epoch != 0:
                lossList.append(runningLoss)
                print(f'100 Batch Cumulative Loss: {runningLoss}')
                runningLoss = 0.0
                pd.DataFrame(lossList,columns=['Loss']).to_csv(self.lossLoc,index=False)
                print(f'Time for 100 Batches: {(time.time()-start)/60}\n---------------------')
                start = time.time()
        torch.save(self.net.state_dict(),self.networkLoc)
        #self.net._save_to_state_dict(self.networkLoc)

    def testNetwork(self,validation=True):
        with torch.no_grad():
            for i, pair in enumerate(self.makePairs(self.validation if validation else self.training)):
                features, labels = self.makeBatchTensors([pair])
                features = features.to(self.device)
                ouputs = self.net(features.float(),test=True)

    def testNetworkAll(self,proportionNeg=10,saveTerms={'GO:0007005','GO:0006302','GO:0007127'},runAll=True,validation=True):
        with torch.no_grad():
            
            def calcPair(pair,termIndex):
                features, labels = self.makeBatchTensors(np.array([pair]))
                features = features.to(self.device)
                outputs = np.array(self.net(features.float(),test=True).cpu(),dtype='float32')
                labels = np.array(labels,dtype=np.intc)
                # print(f'Shape of Labels: {labels.shape}')
                # print(f'Shape of Outputs: {outputs.shape}')
                return([pair[0],pair[1],labels[0,termIndex],outputs[0,termIndex]])

            def calcStats(data):
                def calcMatrix(tp,tn,fp,fn):
                    accuracy = (tp+tn) / (tp+fn+fp+tn)
                    precision = 1 if (tp+fp) == 0 else tp / (tp+fp)
                    recall = 1 if (tp+fn) == 0 else tp / (tp+fn)
                    falsePositiveRate = fn / (fp+tn)
                    selectivity = tn / (tn+fp)
                    return [accuracy,precision,recall,falsePositiveRate,selectivity]
                
                sortedData = data[data[:,3].argsort()[::-1]]
                print(f'Sorted Data: {sortedData}')
                falseNeg = len([genePair for genePair in sortedData if genePair[2] == 1])
                truePos = 0
                trueNeg = len(sortedData) - falseNeg
                falsePos = 0
                

                # statistics = [[truePos,falseNeg,trueNeg,falsePos] + calcMatrix(tp=truePos,tn=trueNeg,fp=falsePos,fn=falseNeg)]
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
            
            def averagePrecision(inputArray):
                precisionArray = np.copy(inputArray)
                for i in range(len(precisionArray)-1,0,-1):
                    if precisionArray[i] > precisionArray[i-1]:
                        precisionArray[i-1] = precisionArray[i]
                return np.mean(precisionArray)

            print("Began Testing the Network")
            allPairs = set([(pair[0],pair[1]) for pair in self.makePairs(self.validation if validation else self.training)])
            leafStatsDist = []
            columnNames = ['Gene A','Gene B','Label','Confidence','True Positive','False Negative','True Negative','False Positive','accuracy','precision','recall','falsePositiveRate','selectivity']
            for i, leaf in enumerate(self.leaves):
                print(f'Testing GO Term: {leaf[0]} ({i} / {len(self.leaves)})')
                if leaf[0] in saveTerms or runAll:
                    posGenes = [gene for gene in self.validation if gene in leaf[1]]
                    if len(posGenes) == 0 or True:
                        posGenes = list(leaf[1])
                    posPairs = self.makePairs(np.array(posGenes))
                    print(f'Pos Genes: {posGenes}')
                    negPairs = np.array([[pair[0],pair[1]] for pair in allPairs - set([(pair[0],pair[1]) for pair in posPairs])])
                    print(f'Pos piars: {posPairs}\nNeg Pairs: {negPairs}')
                    
                    np.random.shuffle(negPairs)
                    negPairs = negPairs[:len(posPairs)*proportionNeg]
                    # print(posPairs[0])
                    # print(negPairs[0])
                    testingPairs = np.concatenate([posPairs,negPairs])

                    #Calculate the data for a term
                    termData = np.array([calcPair(pair,self.GOTermDict[leaf[0]]) for pair in testingPairs],dtype=object)
                    sortedData = termData[termData[:,3].argsort()[::-1]]
                    
                    stats = calcStats(termData)
                    termResults = np.concatenate([sortedData,stats],axis=1)
                    leafStatsDist.append([leaf[0],np.mean(termResults[:,11]),averagePrecision(termResults[:,9])])
                    goTerm = leaf[0].replace(':','-')
                    print('Are we attempting to save')
                    pd.DataFrame(termResults,columns=columnNames).to_csv(f'{self.testLoc}/{goTerm}_stats_fold{self.fold}.csv',index=False)
            if runAll:
                pd.DataFrame(leafStatsDist,columns=['GO Term','AUC','Average Precision']).to_csv(f'{self.testLoc}/GOTermDistribution.csv',index=False)
            


    #Makes input batches with pairs of genes, each pair being a list of two strings
    def makeBatchArray(self,pairs):
        #Returns array with batch size number of random gene pairs
        return pairs[np.random.choice(len(pairs),self.batch,replace=False),:]

    def makeBatchTensors(self,batchArray):
        #Helper function for calculating correlations in list comprehension
        def calcCorr(d,gp):
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
                d = d[d.rfind('\\')+1:]
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
        # print(f'Features: {features}')
        return (features,labels)
        

        


    #Returns array of all pairs of gene from given array of genes
    def makePairs(self,genes):
        pairs = []
        #Loop over all genes
        
        arr = np.array([(genes[i],genes[j]) for i in range(len(genes)) for j in range(i+1,len(genes))])
        return arr
        
        
        #Previous implementation of makePairs

        # for i in range(len(genes)):
        #     #Loop over all genes after gene i, this will result in there being no duplicates
        #     for j in range(i+1,len(genes)):
        #         #Append a tuple of (gene i, gene j)
        #         pairs.append((genes[i],genes[j]))
        # return np.array(pairs)


    def parallelCalc(self,pairs,startIdx,start,threadLabel):
        parArr = np.zeros((len(pairs),len(self.datasets)))
        print(f'Thread {threadLabel} started at time {(time.time()-start)/60} mintues')
        # print(f'Thread {threadLabel} pairs: {len(pairs)}')
        pairStart = time.time()
        for p in range(len(pairs)):
            for d in range(len(self.datasets)):
                parArr[p,d] = self.datasets[d].customCorrelation(pairs[p])
            if p % 100 == 0 and p != 0:
                print(f'Thread {threadLabel} time to calculate 100 pairs: {(time.time()-pairStart)/60} minutes')
                pairStart = time.time()
        print(f'Thread {threadLabel} finished at time {(time.time()-start)/60} minutes')

    def threadsTestSpeed(self,num,numThreads=50):
        pairs = self.makePairs(self.training)[:num]
        start = time.time()

        parArr = np.zeros((len(pairs),len(self.datasets)))
        proportion = len(pairs) / numThreads
        threads = []
        for i in range(numThreads):
            threadPairs = pairs[int(i*proportion):int((i+1)*proportion)] if i != numThreads-1 else pairs[int(i*proportion):]
            threads.append(threading.Thread(target=self.parallelCalc,args=(threadPairs,int(i*proportion),start,i)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print(f'Time to calculate pairs parrallel (threads): {(time.time()-start)/60} minutes')
    
    def executorTestSpeed(self,num,numThreads):
        pairs = self.makePairs(self.training)[:num]
        start = time.time()
        #parArr = np.zeros((len(pairs),len(self.datasets)))

        ex = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count())

        with ex as executor:

            parArr = np.zeros((len(pairs),len(self.datasets)))
            proportion = len(pairs) / numThreads
            futures = []
            for i in range(numThreads):
                threadPairs = pairs[int(i*proportion):int((i+1)*proportion)] if i != numThreads-1 else pairs[int(i*proportion):]
                futures.append(executor.submit(self.parallelCalc,threadPairs,int(i*proportion),start,i))
            finished, _ = concurrent.futures.wait(futures,return_when=concurrent.futures.ALL_COMPLETED)

            print(f'Time to calculate pairs parrallel (executor): {(time.time()-start)/60} minutes')
        
        

    def linearTestSpeed(self,num):
        pairs = self.makePairs(self.training)[:num]
        start = time.time()

        lst =[]
        pairStart = time.time()
        for i, pair in enumerate(pairs,0):
            for dataset in self.datasets:
                lst.append(dataset.customCorrelation(pair))
            if i % 100 == 0 and i != 0:
                print(f'Linear Time to calculate 100 pairs: {(time.time()-pairStart)/60} minutes')
                pairStart = time.time()
        print(f'Time to linear calculate {num} pairs (list): {(time.time()-start)/60} mintues')

    def linearTestSpeedArray(self,num):
        pairs = self.makePairs(self.training)[:num]
        start = time.time()

        arr = np.zeros((len(pairs),len(self.datasets)),dtype=float)
        for p in range(len(pairs)):
            for d in range(len(self.datasets)):
                arr[p,d] = self.datasets[d].customCorrelation(pairs[p])
        print(f'Time to linear calculate {num} pairs (array): {(time.time()-start)/60} mintues')

    def vectorizeTestSpeed(self,num):
        pairs = self.makePairs(self.training)[:num]

        start = time.time()
        def calcCorr(p,d):
            print(f'p: {p}\nd: {d}')
            return self.datasets[int(d)].customCorrelation(pairs[int(p)])
        arr = np.fromfunction(lambda p,d: self.datasets[d].customCorrelation(pairs[p]),(len(pairs),len(self.datasets)),dtype=int)
        print(f'Time to vectorized calculate {num} pairs (array): {(time.time()-start)/60} mintues')

    def testSpeedOfBatch(self,numBatches):
        pairs = self.makePairs(self.training)
        start = time.time()
        for i in range(numBatches):
            arr = self.makeBatchArray(pairs)
            features, labels = self.makeBatchTensors(arr)
        print(f'Time to calculate {numBatches} 20 pair batches: {(time.time()-start)/60} minutes')

    def saveGenesToCSV(self,location):
        pd.DataFrame(np.concatenate((self.training,self.validation),axis=0)).to_csv(location,index=False)



    
        







        







