import torch
# from YeastData import YeastData
import numpy as np
from PrimigNets import PrimegNet

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    # data = YeastData(0.7,4)

    # dataFeatures = data.posData[:,1:len(data.posData[0])]

    # print(data.posData)
    # print(dataFeatures)
    # print(data.posData.shape)
    # print(len(data.negData))
    net = PrimegNet('24x25x1')
    for i in net.parameters():
        print(i)

if __name__ == '__main__':
    main()