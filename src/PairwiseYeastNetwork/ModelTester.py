from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def test(fold,modelName,lr=0.01,batch_size=20,epoch=20000,datasets=430):

    start = time.time()
    # epoch = 10000
	print('Began Loading Data')
    modelData = PairwiseYeastData('Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=datasets,statsDictLoc='./Yeast Resources/Datasets/All Spell/statsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds1.csv')
	print('Finished Loading Data')
    regularTest = PairwiseModel(modelData,fold,'20x10x1','Spell/Test',modelName,lr=lr,batch=batch_size)
    regularTest.trainNetwork(epoch,printLoss=True,saveLoss=True)
    print(f'Training Time: {(time.time()-start)/60} minutes')
    start2 = time.time()
    regularTest.testNetworkValidation(limitNegative=True,negProportion=10)
    print(f'Test Time: {(time.time()-start2)/60} minutes')
    print(f'Total Time: {(time.time()-start)/60} minutes')
    
