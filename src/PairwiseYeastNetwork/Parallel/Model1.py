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
    modelData = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=430,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/ModernFolds1.csv',posGenes='./Yeast Resources/GeneSets/GO0007005_Pos.txt',negGenes='./Yeast Resources/GeneSets/GO0007005_Neg.txt',recur=True,sort=False)
    model = PairwiseModel(modelData,int(sys.argv[1]),f'{sys.argv[2]}x1','Spell/Modern',f'Modern')
    model.trainNetwork(10000,printLoss=True)
    model.testNetworkTraining(limitNegative=True)
    model.testNetworkValidation(limitNegative=True)

    graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/Modern/Modern_{sys.argv[2]}x1_Net_fold',modelData,f'430x{sys.argv[2]}x1',folder=f'Modern_113x{sys.argv[2]}x1',posFile='./Yeast Resources/GeneSets/GO0007005_Pos.txt',negFile='./Yeast Resources/GeneSets/GO0007005_Neg.txt',agnFile='./Yeast Resources/GeneSets/GO0007005_Agn.txt',includeAll=False)
    graph.feedForward(f'Modern_113x{sys.argv[2]}x1_Pairs.csv',fold=int(sys.argv[1]))
    #graph.recombineFolds(f'PosPairsFold','AgnPairsFold',f'Original_113x{sys.argv[2]}x1_Pairs.csv')
    #graph.rankGenes(f'Original_113x{sys.argv[2]}x1_Ranked_IncludeDoubles.csv')


if __name__ == '__main__':
    main()