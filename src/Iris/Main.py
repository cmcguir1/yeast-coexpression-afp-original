import torch
from ModelTester import ModelTester
from IrisNetworks import IrisNet4x2x3, IrisNet4x3x3x3
from IrisData import IrisData
from IrisModel import IrisModel

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#This has to be run in a main thread otherwise you get an error
def main():
    #Check if I need to normalize the data before sending it through the neural network
    test4x3 = ModelTester('4x3')
    test4x2x3 = ModelTester('4x2x3')
    test4x3x3x3 = ModelTester('4x3x3x3')
    test4x3.testModel(5,3)
    # test4x3.testModel(5,30,'./resources/IRIS_4x3_train_6_2.csv','./resources/IRIS_4x3_test_6_2.csv')
    # test4x2x3.testModel(5,30,'./resources/IRIS_4x2x3_train_6_2.csv','./resources/IRIS_4x2x3_test_6_2.csv')
    # test4x3x3x3.testModel(5,30,'./resources/IRIS_4x3x3x3_train_6_2.csv','./resources/IRIS_4x3x3x3_test_6_2.csv')
    

if __name__ == '__main__':
    main()
