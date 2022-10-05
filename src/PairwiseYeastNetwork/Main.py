from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph
import sys
from ComplexModel import ComplexModel
import pandas as pd
import torch
from AllGoModel import AllGoModel
from CorrelationDictionary import CorrelationDictionary
import os

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    
    start = time.time()

    # allModel = AllGoModel(0,'20','Test','TestAll',4)
    # print("Finished Running Model")
    # allModel.net.load_state_dict(torch.load('./Yeast Resources/Pairwise/Spell/Complex/Complex_20_Net_fold1.pth'))
    # print('Finished Loading Network')
    # allModel.testNetworkAll()
    # print(f'Time to Test Network for all GO Terms: {(time.time() - start)/ 60 } minutes')

    # print('Starting 200 Network')
    # allModel200 = AllGoModel(1,'200','Test','TestAll',4)
    # print("Finished Running Model")
    # allModel200.net.load_state_dict(torch.load('./Yeast Resources/Pairwise/Spell/Complex/Complex_200_Net_fold2.pth'))
    # print('Finished Loading Network')
    # allModel200.testNetworkAll()
    # print(f'Time to Test Network for all GO Terms: {(time.time() - start)/ 60 } minutes')

    # print('Starting 200 Network')
    # allModel200 = AllGoModel(2,'200','Test','TestAll',4)
    # print("Finished Running Model")
    # allModel200.net.load_state_dict(torch.load('./Yeast Resources/Pairwise/Spell/Complex/Complex_200_Net_fold3.pth'))
    # print('Finished Loading Network')
    # allModel200.testNetworkAll()
    # print(f'Time to Test Network for all GO Terms: {(time.time() - start)/ 60 } minutes')

    # print('Starting 200 Network')
    # allModel200 = AllGoModel(3,'200','Test','TestAll',4)
    # print("Finished Running Model")
    # allModel200.net.load_state_dict(torch.load('./Yeast Resources/Pairwise/Spell/Complex/Complex_200_Net_fold4.pth'))
    # print('Finished Loading Network')
    # allModel200.testNetworkAll()
    # print(f'Time to Test Network for all GO Terms: {(time.time() - start)/ 60 } minutes')
    
    # data = PairwiseYeastData(f'Yeast Resources/Datasets/All Spell/all spell datasets',4,subset=200000,numDatasets=430,statsDictLoc='./Yeast Resources/Datasets/All Spell/revisedStatsDict.csv',recalc=False,foldFile='./Yeast Resources/Datasets/All Spell/GeneFolds3.csv',posGenes='./Yeast Resources/positives_00_go04-15-07.txt',negGenes='./Yeast Resources/negatives_00_go04-15-07.txt',recur=True,sort=False)
    # print('Finsihed Initializing Data')
    # graph = YeastGraph(f'./Yeast Resources/Pairwise/Spell/430Standard/Regular_20x1_Net_fold',data,f'430x20x1',folder=f'Standard_430x20x1',posFile='./Yeast Resources/positives_00_go04-15-07.txt',negFile='./Yeast Resources/negatives_00_go04-15-07.txt',agnFile='./Yeast Resources/agnostic_01_underannotated.txt',includeAll=False)
    # print('Finished Initializing Network')
    # graph.saveGenesToCSV('./src/PairwiseYeastNetwork/allGenes.csv')
    
    corr = CorrelationDictionary()
    corr.unifyCorrelations('/home/cmcguir1/data/YeastMemMap/YeastCorrDictionary.dat')
    # print(len(corr.expDataset.datasets))
    # for i in range(int(sys.argv[2]),int(sys.argv[2])+50):
    #     if i < 430:
    #         dataset = corr.expDataset.datasets[i]
    #         corr.calculateDataset(datasetIndex=i,location=f'{sys.argv[1]}/{dataset.dataFile}_corrDict.dat')



if __name__ == '__main__':
    main()
