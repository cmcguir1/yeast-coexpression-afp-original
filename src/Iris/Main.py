import torch
from IrisData import IrisData
from IrisModel import IrisModel

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#This has to be run in a main thread otherwise you get an error
def main():
    #Check if I need to normalize the data before sending it through the neural network
    irisData = IrisData(0.7,'./resources/IRIS.csv')
    testNetwork = IrisModel(irisData)
    testNetwork.testNetworkAccuracyTesting()
    testNetwork.trainNetwork(5)
    testNetwork.testNetworkAccuracyTesting()
    testNetwork.trainNetwork(5)
    testNetwork.testNetworkAccuracyTesting()
    testNetwork.trainNetwork(5)
    testNetwork.testNetworkAccuracyTesting()
    
    



if __name__ == '__main__':
    main()
