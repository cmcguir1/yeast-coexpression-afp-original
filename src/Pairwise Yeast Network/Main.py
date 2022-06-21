from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    #This comment should appear on github now

    # folds = GeneFolds(numFolds=4)
    # folds.writeToCsv('./Yeast Resources/Datasets/All Spell/GeneFolds1.csv')



    start = time.time()
    epoch = 10000
    modelData = PairwiseYeastData('Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=430,statsDictLoc='./Yeast Resources/Datasets/All Spell/statsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds1.csv')
    #modelData.saveStatistics('./Yeast Resources/Datasets/All Spell/statsDict.csv')
    print(f'Time to load datasets: {(time.time()-start)/60} minutes')

    regularTest = []
    for i in range(4):
        regularTest.append(PairwiseModel(modelData,i,'20x1','Spell/Test','Regular430'))
        # noRegularTest.append(PairwiseModel(modelData,i,'20x10x1','Spell/Test','NoRegular50'))
    for model in regularTest:
        model.trainNetwork(epoch,printLoss=True,lossFile='./Yeast Resources/Datasets/All Spell/Regular430_Loss.csv')
        model.testNetworkValidation(limitNegative=True)
    # for model in noRegularTest:
    #     model.trainNetwork(epoch,printLoss=True,regularize=False)
    #     model.testNetworkValidation(regularize=False,limitNegative=True)
    







    

if __name__ == '__main__':
    main()