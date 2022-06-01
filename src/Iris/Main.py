import torch
from IrisNetworks import IrisNet4x2x3, IrisNet4x3x3x3
from IrisData import IrisData
from IrisModel import IrisModel

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#This has to be run in a main thread otherwise you get an error
def main():
    #Check if I need to normalize the data before sending it through the neural network
    dataPath = './resources/IRIS.csv'
    irisNet4x3 = IrisModel(dataPath,network=IrisNet4x2x3())
    irisNet4x2x3 = IrisModel(dataPath,network=IrisNet4x2x3())
    irisNet4x3x3x3 = IrisModel(dataPath,network=IrisNet4x3x3x3())

    # irisNet4x3.trainNetwork(10,shouldPrint=True)
    # irisNet4x2x3.trainNetwork(10,shouldPrint=True)
    # irisNet4x3x3x3.trainNetwork(45)
    # irisNet4x3.testNetworkAccuracyTraining()
    # irisNet4x3.testNetworkAccuracyTesting()
    # irisNet4x2x3.testNetworkAccuracyTraining()
    # irisNet4x2x3.testNetworkAccuracyTesting()
    # irisNet4x3x3x3.testNetworkAccuracyTraining()
    # irisNet4x3x3x3.testNetworkAccuracyTesting()
    



if __name__ == '__main__':
    main()
