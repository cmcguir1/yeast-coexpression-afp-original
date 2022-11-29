import numpy as np
import pandas as pd
import torch
from AllGoModel import AllGoModel
import os
from FlexNet import FlexNet

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves

class AllGoGraph(AllGoModel):
    def __init__(self,networkPath,data,structure,folder,numfolds=4):
        #Intialize file path for folder where results will be saved
        self.path = f'./Yeast Resources/GraphResults/{folder}'
        if(not os.path.exists(self.path)):
            os.mkdir(self.path)

        #Intiailize list of networks and device tensor will be calculated on
        self.numFolds = numfolds
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.nets = []
        for i in range(numfolds):
            net = FlexNet(structure)
            net.load_state_dict(torch.load(f'{networkPath}{i+1}.pth'))
            self.nets.append(net)

        

    def feedForward(self,term='GO:0007005'):
        pass
