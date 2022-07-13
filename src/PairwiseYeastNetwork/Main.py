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
import os

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    
    # jin = AllGoModel(0,'./Yeast Resources/Datasets/All Spell/complexgeneFolds1.csv',20,'ComplexTest','AllGoTest')
    # jin.trainNetwork(2)
    if(os.path.exists('./Yeast Resources/NewFolderTest')):
        print('Folder already exists')
    else:
        os.mkdir('./Yeast Resources/NewFolderTest')
    

    

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

    #data = PairwiseYeastData('./Yeast Resources/Datasets/Primig and Brem',4,'./Yeast Resources/Datasets/All Spell/GeneFolds1.csv',sort=False,recur=False,numDatasets=430,subset=10000)
    # graph = YeastGraph('./Yeast Networks/Spell/Test/Regular430_20x1_fold1_Val.pth',modelData,'430x20x1',posFile='./Yeast Resources/test_positives.txt',negFile='./Yeast Resources/test_negatives.txt',agnFile='./Yeast Resources/test_agnostics.txt')
    # graph.feedForward('./Yeast Resources/Test_Graph.csv')
    # graph.rankGenes('./Yeast Resources/Test_Rank.csv')

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



    







    

if __name__ == '__main__':
    main()
