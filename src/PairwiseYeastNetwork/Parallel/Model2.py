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
    modelData = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=430,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds3.csv',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',recur=True,sort=False)
    # model = PairwiseModel(modelData,int(sys.argv[1]),f'{sys.argv[2]}x1','Spell/OriginalRerun',f'Original')
    # model.trainNetwork(10000,printLoss=True)
    # model.testNetworkTraining(limitNegative=True)
    # model.testNetworkValidation(limitNegative=True)

    graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/430Standard/Regular_{sys.argv[2]}x1_Net_fold',modelData,f'430x{sys.argv[2]}x1',folder=f'Standard_430x{sys.argv[2]}x1',posFile='./Yeast Resources/positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt',includeAll=False)
    #graph.feedForward(f'Standard_430x{sys.argv[2]}x1_Pairs.csv',fold=int(sys.argv[1]))
    #graph.recombineFolds(f'PosPairsFold','AgnPairsFold',f'Standard_430x{sys.argv[2]}x1_Pairs.csv')
    # graph.saveGenesToCSV('./src/PairwiseYeastNetwork/allGenes.csv')
    # graph.rankGenes(f'Standard_430x{sys.argv[2]}x1_Ranked.csv')
    # for i in range(4):
    #     graph.filterAgn(f'./Yeast Resources/GraphResults/Original_Rerun_113x20x1/PosPairsFold{i+1}.csv')


if __name__ == '__main__':
    main()