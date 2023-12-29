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

genes = getGenes('GO:0006869',dataset='original')
print(genes)
print(len(genes))


