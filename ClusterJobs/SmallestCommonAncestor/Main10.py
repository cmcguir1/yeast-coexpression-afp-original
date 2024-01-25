from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time
from GeneFolds import GeneFolds
from YeastGraph import YeastGraph
from AllGOGraph import AllGoGraph
import sys
from ComplexModel import ComplexModel
import pandas as pd
import torch
from AllGoModel import AllGoModel
from CorrelationDictionary import CorrelationDictionary
import os

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes
from GOParser import GOParser

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    
    go = GOParser('2007')
    yorf = list(go.onto.yorfs.keys())


    
    pairs = np.ndarray((int(len(yorf)*(len(yorf)-1)/2),3),dtype=object)
    index = 0
    for i in range(len(yorf)):
        print(i)
        for j in range(i+1,len(yorf)):
            pairs[index,0] = yorf[i]
            pairs[index,1] = yorf[j]
            pairs[index,2] = go.smallestCommonAncestor(yorf[i],yorf[j])
            index += 1

    np.save('./src/PairwiseYeastNetwork/Pairs_SmallestCommonAncestor.npy',pairs)
        









if __name__ == '__main__':
    main()

