from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph
import sys
from ComplexModel import ComplexModel
import pandas as pd
import torch
from AllGoModel import AllGoModel
from CorrelationDictionary import CorrelationDictionary
import os

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    
    # jin = AllGoModel(0,'./Yeast Resources/Datasets/All Spell/complexgeneFolds1.csv',20,'ComplexTest','AllGoTest')
    # jin.trainNetwork(2)
    # modelData = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/original',4,subset=200000,numDatasets=113,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds3.csv',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',recur=False,sort=False)
    # # model = PairwiseModel(modelData,int(sys.argv[1]),f'{sys.argv[2]}x1','Spell/OriginalRerun',f'Original')
    # # model.trainNetwork(10000,printLoss=True)
    # # model.testNetworkTraining(limitNegative=True)
    # # model.testNetworkValidation(limitNegative=True)

    # graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/OriginalRerun/Original_{20}x1_Net_fold',modelData,f'113x{20}x1',folder=f'Original_113x{20}x1',posFile='./Yeast Resources/positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt',includeAll=False)
    # #graph.compareFolds('./Yeast Resources/GraphResults/Test/FoldComparison.csv',cutoff=4000)
    # graph.compareGOTerms('./Yeast Resources/positives_00_go04-15-07.txt','./Yeast Resources/GeneSets/GO0006302_Pos.txt')
    # graph.feedForward(f'Original_113x{sys.argv[2]}x1_Pairs.csv',fold=int(sys.argv[1]))
    # graph.recombineFolds(f'PosPairsFold','AgnPairsFold',f'Original_113x{sys.argv[2]}x1_Pairs.csv')
    # graph.rankGenes(f'Original_113x{sys.argv[2]}x1_Ranked.csv')

    
    

    

    # # regularTest = []
    # # for i in range(4):
    # regularTest = PairwiseModel(modelData,0,'20x10x1','Spell/Test','SpeedTest',lr=0.1,batch=50)
    # regularTest.trainNetwork(10000,printLoss=True,lossFile='./Yeast Resources/Datasets/All Spell/SpeedTestLoss1.csv')
    # print(f'Training Time: {(time.time()-start)/60} minutes')
    # start = time.time()
    # regularTest.testNetworkValidation(limitNegative=True,negProportion=10)
    # print(f'Total Time: {(time.time()-start)/60} minutes')
    # #     # noRegularTest.append(PairwiseModel(modelData,i,'20x10x1','Spell/Test','NoRegular50'))
    # for model in regularTest:
    #     model.trainNetwork(epoch,printLoss=True,lossFile='./Yeast Resources/Datasets/All Spell/Regular430_Loss.csv')
    #     model.testNetworkValidation(limitNegative=True)
    # for model in noRegularTest:
    #     model.trainNetwork(epoch,printLoss=True,regularize=False)
    #     model.testNetworkValidation(regularize=False,limitNegative=True)

    # data = PairwiseYeastData('./Yeast Resources/Datasets/Primig and Brem',4,'./Yeast Resources/Datasets/All Spell/GeneFolds1.csv',sort=False,recur=False,numDatasets=430,subset=10000)
    # graph = YeastGraph('./Yeast Networks/Spell/Test/Regular430_20x1_fold1_Val.pth',data,'430x20x1',posFile='./Yeast Resources/test_positives.txt',negFile='./Yeast Resources/test_negatives.txt',agnFile='./Yeast Resources/test_agnostics.txt')
    # graph.feedForward('./Yeast Resources/Test_Graph.csv')
    # graph.rankGenes('./Yeast Resources/Test_Rank.csv')
    # graph.saveGenesToCSV('./src/PairwiseYeastNetwork/allGenes.csv')


    # dataArray = np.array([[13,5],[12,23],[20,21]])
    # print(dataArray)

    # sortedArray = dataArray[dataArray[:,1].argsort()[::-1]]
    # reverse = np.argsort(-1*sortedArray)
    # print(sortedArray)
    # print(reverse)
    # start = time.time()
    # complexModel = ComplexModel(0,4,'10','Spell/Test','ComplexTest')
    # print(f'Overhead : {(time.time()-start)/60}')
    # complexModel.trainNetwork(10000,printLoss=True)

    # allModel = AllGoModel(0,'20','Test','TestAll',4)
    # allModel.vectorizeTestSpeed(1000)
    # allModel.linearTestSpeed(1000)
    # allModel.executorTestSpeed(3000,numThreads=10)
    # allModel.threadsTestSpeed(10000,numThreads=10)
    # allModel.threadsTestSpeed(5000,numThreads=20)

    #allModel.testSpeedOfBatch(500)
    # allModel.saveGenesToCSV()
    
    # data = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=430,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds3.csv',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',recur=True,sort=False)
    # print('Finsihed Initializing Data')
    # graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/430Standard/Regular_20x1_Net_fold',data,f'430x20x1',folder=f'Standard_430x20x1',posFile='./Yeast Resources/positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt',includeAll=False)
    # print('Finished Initializing Network')
    # graph.saveGenesToCSV('./src/PairwiseYeastNetwork/allGenes.csv')
    
    corr = CorrelationDictionary()
    dataset = corr.expDataset.datasets[int(sys.argv[2])]
    corr.calculateDataset(datasetIndex=int(sys.argv[2]),location=f'./{sys.argv[1]}/{dataset.dataFile}_corrDict.dat')



if __name__ == '__main__':
    main()
