from turtle import shape
from sqlalchemy import false
import torch
# from YeastData import YeastData
import numpy as np
from PrimigNets import PrimegNet
from YeastModel import YeastModel

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    model = YeastModel(fold=0,percentTest=0.2,numFolds=4,structure='24x25x1',lr=0.01,momentum=0.9,batch_size=10)
    model.trainNetwork(20000)
    

if __name__ == '__main__':
    main()