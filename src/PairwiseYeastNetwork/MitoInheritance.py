
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
    
    
    folderName = f'Spell/SingleTerm_{sys.argv[2]}'

    
    term = 'GO:0007005'

    
    
    
    graph = YeastGraph(f'Yeast Resources/Pairwise/Spell/SingleTerm_{sys.argv[2]}/{term[0:2]}{term[3:]}_{sys.argv[2]}x1_Net_fold',f'113x{sys.argv[2]}x1',term,f'SingleTerms_{sys.argv[2]}')
    graph.forward(int(sys.argv[1]),calcAll=True,calcPos=True,calcAgn=True)
    # graph.recombineFolds(agn=True)
    # graph.rankGenes()



if __name__ == '__main__':
    main()
