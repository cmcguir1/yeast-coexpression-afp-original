from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def test(fold,modelName,lr=0.01,batch_size=20,epoch=5000,datasets=430,structure='20x1',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds1.csv',folderName='Spell/Test',dataFolder='all spell datasets'):

    start = time.time()
    # epoch = 10000
    print('Began Loading Data',flush=True)
    modelData = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/{dataFolder}',4,subset=200000,numDatasets=datasets,statsDictLoc='./Yeast Resources/Datasets/All Spell/statsDict.csv',recalc=False,foldFile=foldFile,posGenes=posGenes,negGenes=negGenes)
    print('Finished Loading Data',flush=True)
    regularTest = PairwiseModel(modelData,fold,structure,folderName,modelName,lr=lr,batch=batch_size)
    regularTest.trainNetwork(epoch,printLoss=True,saveLoss=True)
    print(f'Training Time: {(time.time()-start)/60} minutes',flush=True)
    start2 = time.time()
    regularTest.testNetworkValidation(limitNegative=True,negProportion=10)
    regularTest.testNetworkTraining(limitNegative=True,negProportion=10)
    print(f'Test Time: {(time.time()-start2)/60} minutes')
    print(f'Total Time: {(time.time()-start)/60} minutes')
    
