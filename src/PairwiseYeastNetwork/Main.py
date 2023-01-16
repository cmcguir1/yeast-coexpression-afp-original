
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

    #Structure Tests

    GOTest = AllGoModel(int(sys.argv[1]),'200','Regular','Regular',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv')
    # GOTest = AllGoModel(int(sys.argv[1]),'200','Regular','Regular',foldFile='./src/PairwiseYeastNetwork/AllGOGeneFold1.csv',memMapLoc='../YeastMemMap/YeastCorrDictionary.dat')
    GOTest.net.load_state_dict(torch.load(f'./Yeast Resources/Pairwise/Spell/Regular/Regular_430x200x92_Net_fold{int(sys.argv[1]) + 1}.pth'))
    #GOTest.saveGenesToCSV('./src/PairwiseYeastNetwork/AllGOGeneFold1.csv')
    #GOTest.trainNetwork(10000)
    GOTest.testNetworkAll(runAll=True)
    #GOTest.testNetworkAll(runAll=True,validation=False)

    # GO = AllGoModel(0,'200','AllOriginalTest','OriginalDatasets',ontologyDataset='original')
    # GO.trainNetwork(1000)




if __name__ == '__main__':
    main()
