from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():


    # for i in range(2):
    #     printModelData = PairwiseYeastData('Yeast Resources/Datasets/Primig and Brem',4,subset=10000,recur=False)
    # print(f'Time: {(time.time()-start)/60}')
    # start = time.time()
    # for i in range(2):
    #     printModelData = PairwiseYeastData('Yeast Resources/Datasets/Primig and Brem',4,subset=100000,recur=False)
    # print(f'Time: {(time.time()-start)/60}')
    # start = time.time()
    # printModelData = PairwiseYeastData('Yeast Resources/Datasets/Primig and Brem',4,subset=1000000,recur=False)
    # print(f'Time: {(time.time()-start)/60}')
    # start = time.time()
    # printModelData = PairwiseYeastData('Yeast Resources/Datasets/Primig and Brem',4,subset=11179356,recur=False)
    # print(f'Time: {(time.time()-start)/60}')


    start = time.time()
    epoch = 100000
    modelData = PairwiseYeastData('Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=100000,numDatasets=60,statsDictLoc='./Yeast Resources/Datasets/All Spell/statsDict.csv',recalc=True)
    #modelData.saveStatistics('./Yeast Resources/Datasets/All Spell/statsDict.csv')
    print(f'Time to load datasets: {(time.time()-start)/60} minutes')

    # regularTest = []
    # noRegularTest = []
    # for i in range(4):
    #     regularTest.append(PairwiseModel(modelData,i,'20x1','Pairwise Test','Regular'))
    #     noRegularTest.append(PairwiseModel(modelData,i,'20x1','Pairwise Test','NoRegular'))
    # for model in noRegularTest:
    #     model.trainNetwork(epoch,printLoss=True,printTensors=True,regularize=False)
    #     model.testNetworkValidation(regularize=False)
    # for model in regularTest:
    #     model.trainNetwork(epoch)
    #     model.testNetwork()

    # syntheticData = PairwiseYeastData('./Yeast Resources/Datasets/Synthetic/Medium 36-264',4,subset=10000,numDatasets=5,recur=False,sort=False,filterMissingGenes=True)
    # syntheticModel = PairwiseModel(syntheticData,0,'1','Pairwise/Synthetic/Test','MedTest')
    # syntheticModel.trainNetwork(1000,printLoss=True,printTensors=True)
    # syntheticModel.testNetworkValidation()

    # smallData = PairwiseYeastData('./Yeast Resources/Datasets/Primig and Brem',4,subset=100000,numDatasets=3,recur=False,sort=False,filterMissingGenes=True)
    # smallModel = PairwiseModel(smallData,0,'10x10x1','Pairwise/Primig and Brem Test','TestResult')
    # smallModel.trainNetwork(10000,printLoss=True,printTensors=True)
    # smallModel.testNetworkValidation()



    # printModel = PairwiseModel(printModelData,0,'20x1','Spell/Test','TestRun')
    # printModel.trainNetwork(10000,printLoss=True)

    # GalitskiData = PairwiseYeastData('Yeast Resources/Datasets/All Spell/all spell datasets/Wyrick_1999_PMID_10586882',4,subset=100000,numDatasets=1,recur=False)



    

if __name__ == '__main__':
    main()