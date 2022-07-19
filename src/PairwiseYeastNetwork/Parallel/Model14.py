import sys

from numpy import double
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test
from PairwiseModel import PairwiseModel
from PairwiseYeastData import PairwiseYeastData
from YeastGraph import YeastGraph

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    modelData = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/original',4,subset=200000,numDatasets=113,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds3.csv',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',recur=False,sort=False)
    # model = PairwiseModel(modelData,int(sys.argv[1]),f'{sys.argv[2]}x1','Spell/OriginalRerun',f'Original')
    # model.trainNetwork(10000,printLoss=True)
    # model.testNetworkTraining(limitNegative=True)
    # model.testNetworkValidation(limitNegative=True)
    struct = '20'
    for i in range(4):
        graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/OriginalRerun/Original_{struct}x1_Net_fold',modelData,f'113x{struct}x1',folder=f'Original_113x{struct}x1',posFile='./Yeast Resources/positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt',includeAll=False)
        graph.feedForward(f'Original_113x{struct}x1_Pairs.csv',fold=int(i))
    # struct = '50'
    # for i in range(4):
    #     graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/OriginalRerun/Original_{struct}x1_Net_fold',modelData,f'113x{struct}x1',folder=f'Original_113x{struct}x1',posFile='./Yeast Resources/positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt',includeAll=False)
    #     graph.feedForward(f'Original_113x{struct}x1_Pairs.csv',fold=int(i))
    struct = '100'
    for i in range(4):
        graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/OriginalRerun/Original_{struct}x1_Net_fold',modelData,f'113x{struct}x1',folder=f'Original_113x{struct}x1',posFile='./Yeast Resources/positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt',includeAll=False)
        graph.feedForward(f'Original_113x{struct}x1_Pairs.csv',fold=int(i))
    # graph.rankGenes(f'Original_113x{sys.argv[2]}x1_Ranked.csv')


if __name__ == '__main__':
    main()