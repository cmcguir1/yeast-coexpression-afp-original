from turtle import shape
from sqlalchemy import false
import torch
# from YeastData import YeastData
import numpy as np
from PrimigNets import PrimegNet
from YeastModel import YeastModel
from YeastData import YeastData
import time


# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    start = time.time()
    prim = []
    brem24 = []
    epochs = 5000
    for j in range(10):
        primData = YeastData(0.2,4,'./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl')
        bremData = YeastData(0.2,4,'./Yeast Resources/2010.Brem05_orig.flt.knn.avg.24.txt')
        for i in range(4):
            prim.append(YeastModel(fold=i,yeastData=primData,structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName=f'Primeg_dataset{j+1}'))
            brem24.append(YeastModel(fold=i,yeastData=bremData,structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName=f'Brem24_dataset{j+1}'))
    for model in prim:
        model.trainNetwork(epochs)
        model.testNetworkVal(save=True)
    for model in brem24:
        model.trainNetwork(epochs)
        model.testNetworkVal(save=True)
        
    # prim = []
    # brem24 = []
    # synPosMed = []
    # synPosStrong =[]
    # synNeg = []
    # for i in range(4):
    #     prim.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName=f'Primeg_dataset{i}'))
    #     brem24.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Brem05_orig.flt.knn.avg.24.txt',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName=f'Brem24_dataset{i}'))
    #     synPosMed.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/Synthetic_PositiveControl_Medium.txt',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='SynPosMed'))
    #     synPosStrong.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/Synthetic_PositiveControl_Strong.txt',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='SynPosStrong'))
    #     synNeg.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/Synthetic_NegativeControl.txt',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='SynNeg'))

    # epochs = 120000
    # for model in prim:
    #     model.trainNetwork(epochs)
    #     model.testNetworkVal(save=True)
    # for model in brem24:
    #     model.trainNetwork(epochs)
    #     model.testNetworkVal(save=True)
    # for model in synPosMed:
    #     model.trainNetwork(epochs)
    #     model.testNetworkVal(save=True)
    # for model in synPosStrong:
    #     model.trainNetwork(epochs)
    #     model.testNetworkVal(save=True)
    # for model in synNeg:
    #     model.trainNetwork(epochs)
    #     model.testNetworkVal(save=True)

    end = time.time()
    print(f'Total time in minutes: {((end-start)/60):3f}')

    
    
    
    

    # epoch = 15000
    # primegMedium = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Example')
    # brem24Medium = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='Yeast Resources/2010.Brem05_orig.flt.knn.avg.24.txt',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Brem24_FixedMat')
    # primegMedium.saveFoldGeneVal()
    
if __name__ == '__main__':
    main()