import torch
from CrossValidator import CrossValidator
from BostonModel import BostonModel
from BostonData import BostonData

#This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    #Ask Hibbs if I should normalize my outputs in the dataset
    crossVal = CrossValidator(4,'13x5x5x1')
    crossVal.crossValidate(3)
    # data = BostonData(4)
    # train, val = data.getFoldDatasets(0)
    # model = BostonModel(train,val,'')
    # print(f'Percent Error: {model.testNetworkTrain()}')
    # for i in range(10):
    #     model.trainNetwork(1)
    #     print(f'Percent Error: {model.testNetworkTrain()}')

if __name__ == '__main__':
    main()