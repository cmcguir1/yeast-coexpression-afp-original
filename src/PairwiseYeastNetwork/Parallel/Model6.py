import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test
from PairwiseModel import PairwiseModel
from PairwiseYeastData import PairwiseYeastData

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    modelData = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=430,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds1.csv',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',recur=True,sort=False)
    for i in range(4):
        model = PairwiseModel(modelData,i,'200x1','Spell/Activation',modelName=sys.argv[1],activation=sys.argv[1])
        model.trainNetwork(20000,printLoss=True)
        model.testNetworkTraining(limitNegative=True)
        model.testNetworkValidation(limitNegative=True)


if __name__ == '__main__':
    main()