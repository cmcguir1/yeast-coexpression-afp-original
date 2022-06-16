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


    # start = time.time()
    # printModelData = PairwiseYeastData('Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=10000,numDatasets=25)
    # print(f'Time to load datasets: {(time.time()-start)/50} minutes')

    # printModel = PairwiseModel(printModelData,0,'20x1','Spell/Test','TestRun')
    # printModel.trainNetwork(10000,printLoss=True)

    GalitskiData = PairwiseYeastData('Yeast Resources/Datasets/All Spell/all spell datasets/Wyrick_1999_PMID_10586882',4,subset=100000,numDatasets=1,recur=False)


    


    # printModelData.calculateCorrelations()
    # printModel = PairwiseModel(printModelData,0,'1','Synthetic/Medium 36-264','PrintTest')
    # printModel.trainNetwork(1000,printLoss=True,printTensors=True)
    # printModel.testNetworkValidation(save=False)
    

if __name__ == '__main__':
    main()