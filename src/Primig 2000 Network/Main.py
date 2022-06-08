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
    # crossValPrim = []
    # crossValBrem24 = []
    # crossValBremAll = []
    # for i in range(4):
    #     crossValPrim.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x25x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Primeg'))
    #     crossValBrem24.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='Yeast Resources/2010.Brem05_orig.flt.knn.avg.24.txt',structure='24x25x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Brem24'))
    #     crossValBremAll.append(YeastModel(fold=i,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Brem05_orig.flt.knn.avg.all.txt',structure='113x25x1',lr=0.01,momentum=0.9,batch_size=20,dataName='BremAll'))
    
    # epochs = 15000
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

    # for model in crossValBremAll:
    #     model.trainNetwork(epochs)
    #     model.testNetworkTrain()
    #     model.testNetworkVal()
    #     model.testNetworkTest()

    epoch = 15000
    primegMedium = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Primeg_FixedMatrix')
    # primegComplex = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x15x10x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Primeg')
    brem24Medium = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='Yeast Resources/2010.Brem05_orig.flt.knn.avg.24.txt',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Brem24_FixedMat')
    # brem24Complex = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='Yeast Resources/2010.Brem05_orig.flt.knn.avg.24.txt',structure='24x15x10x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Brem24')
    # bremAllMedium = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Brem05_orig.flt.knn.avg.all.txt',structure='113x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='BremAll')
    # bremAllComplex = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Brem05_orig.flt.knn.avg.all.txt',structure='113x15x10x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='BremAll')
    # modelList = [primegMedium,primegComplex,brem24Medium,brem24Complex,bremAllMedium,bremAllComplex]
    # for model in modelList:
    #     print('Hello')
    #     model.trainNetwork(epoch)
    #     model.testNetworkVal()
    # primegMedium.trainNetwork(10000)
    # primegMedium.testNetworkVal()
    brem24Medium.trainNetwork(10000)
    brem24Medium.testNetworkVal()

    

    # model = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x20x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Primeg')
    # model.trainNetwork(100000,collectData=True,filePath='./Yeast Resources/PrimegConvergence5.csv')
    # model.testNetworkVal()
    # model2 = YeastModel(fold=0,percentTest=0.2,numFolds=4,dataPath='./Yeast Resources/2010.Primig00.filter.flt.knn.avg.div.log.pcl',structure='24x15x10x8x1',lr=0.01,momentum=0.9,batch_size=20,dataName='Primeg')
    # model2.trainNetwork(25000,collectData=True,filePath='./Yeast Resources/PrimegConvergence6.csv')
    # model2.testNetworkVal()
if __name__ == '__main__':
    main()