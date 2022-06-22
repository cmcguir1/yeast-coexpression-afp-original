from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    start = time.time()
    # epoch = 10000
    modelData = PairwiseYeastData('Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=50,statsDictLoc='./Yeast Resources/Datasets/All Spell/statsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds1.csv')
    #modelData.saveStatistics('./Yeast Resources/Datasets/All Spell/statsDict.csv')
    regularTest = PairwiseModel(modelData,2,'20x10x1','Spell/Test','SpeedTest',lr=0.1,batch=50)
    regularTest.trainNetwork(10000,printLoss=True,lossFile='./Yeast Resources/All Spell/SpeedTestLoss3.csv')
    print(f'Training Time: {(time.time()-start)/60} minutes')
    start = time.time()
    regularTest.testNetworkValidation()
    print(f'Total Time: {(time.time()-start)/60} minutes')
    







    

if __name__ == '__main__':
    main()