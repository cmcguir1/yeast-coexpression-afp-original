from __future__ import generator_stop
import sys
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import time
import os

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes
rng = np.random.default_rng()
arr = np.zeros((430,21690990),dtype=np.float16)
for i in range(430):
    print(i)
    for j in range(21690990):
        arr[i,j] = rng.standard_normal()
np.save('../YeastDict_Random.npy',arr)


