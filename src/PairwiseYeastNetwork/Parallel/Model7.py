import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')

from ModelTester import test
from ComplexModel import ComplexModel
import torch
from PairwiseYeastData import PairwiseYeastData
from YeastGraph import YeastGraph

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    
    modelData = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=430,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds1.csv',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',recur=True,sort=False)
    graph = YeastGraph('./Yeast Resources/Pairwise/Spell/Dropout/InputDropout_0_200x1_Net_fold1.pth',modelData,'430x200x1',posFile='./Yeast Resources\positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt')
    graph.feedForward('./Yeast Resources/GraphResults/TestFeedForward.csv')
    graph.rankGenes('./Yeast Resources/GraphResults/TestRankGenes.csv')

if __name__ == '__main__':
    main()