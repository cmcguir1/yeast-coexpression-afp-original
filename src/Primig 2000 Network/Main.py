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
    crossValPrim = []
    crossValBrem24 = []
    crossValBremAll = []
    for i in range(4):
        crossValPrim.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x25x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Test_Primeg'))
        crossValBrem24.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='Yeast Resources/2010.Brem05_orig.flt.knn.avg.24.txt',structure='24x25x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Test_Brem24'))
        crossValBremAll.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Brem05_orig.flt.knn.avg.all.txt',structure='113x25x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Test_BremAll'))
    
    epochs = 1000
    # for model in crossValPrim:
    #     model.trainNetwork(epochs)
    #     model.testNetworkTrain()
    #     model.testNetworkVal()
    #     model.testNetworkTest()

    # for model in crossValBrem24:
    #     model.trainNetwork(epochs)
    #     model.testNetworkTrain()
    #     model.testNetworkVal()
    #     model.testNetworkTest()

    for model in crossValBremAll:
        model.trainNetwork(epochs)
        model.testNetworkTrain()
        model.testNetworkVal()
        model.testNetworkTest()

    # model = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x25x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Primeg')
    # model.trainNetwork(50000,collectData=True,filePath='./Yeast Resources/PrimegConvergence2.csv')
    #model.testNetworkVal()
if __name__ == '__main__':
    main()