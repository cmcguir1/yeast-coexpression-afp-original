import torch
import numpy as np
from FocalLoss import FocalLoss
from CustomCrossEntropyLoss import CustomCrossEntropyLoss
import torch.nn.functional as F
import pandas as pd
import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

# redo = np.memmap()


dict = {}
dict[1] = 'one'
dict[2] = 'two'
dict[3] = 'three'

print(dict.items())