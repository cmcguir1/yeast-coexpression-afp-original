from pyparsing import oneOf
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

    # fold = int(sys.argv[1]) % 4
    # size = 20 if int(sys.argv[1]) <= 3 else 200

    # allModel = AllGoModel(fold,f'{size}','Test','MitoOrgTest',4)
    # print("Finished Running Model")
    # allModel.net.load_state_dict(torch.load(f'./Yeast Resources/Pairwise/Spell/Complex/Complex_{size}_Net_fold1.pth'))
    # print('Finished Loading Network')
    # allModel.testNetworkAll(runAll=False)
    # #allModel.testNetworkAll(runAll=True)
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

    # allModel200.trainNetwork(10000)
    # print('Finished Loading Network')
    # allModel200.testNetworkAll()
    # print(f'Time to Test Network for all GO Terms: {(time.time() - start)/ 60 } minutes')
    
    
    # corr = CorrelationDictionary()
    # corr.unifyCorrelations('/home/cmcguir1/data/YeastMemMap/YeastCorrDictionary.dat')
    # print(len(corr.expDataset.datasets))
    # for i in range(int(sys.argv[2]),int(sys.argv[2])+50):
    #     if i < 430:
    #         dataset = corr.expDataset.datasets[i]
    #         corr.calculateDataset(datasetIndex=i,location=f'{sys.argv[1]}/{dataset.dataFile}_corrDict.dat')

    # corr = CorrelationDictionary()
    # print(len(corr.memMap[0]))
    # print(corr.memMap[0])
    # allGoModel = AllGoModel(0,'20','MemMapTest','MemMapTest3',4)
    # allGoModel.trainNetwork(10000)
    # print(f'Time to Train Network for 10,000 epochs: {(time.time() - start) / 60} minutes')
    if(sys.argv[3] == 'r'):
        regularize = True
    else:
        regularize = False
    GOTest = AllGoModel(int(sys.argv[2]),'200','Test',sys.argv[1],ontologyDataset=sys.argv[1],regularize=regularize,memMapLoc='../YeastMemMap/YeastCorrelationDictionary.dat')
    GOTest.trainNetwork(10000)
    GOTest.testNetworkAll(runAll=False)




if __name__ == '__main__':
    main()
