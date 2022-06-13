from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np
import time

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    # start = time.time()
    # data = PairwiseYeastData('./Yeast Resources/Datasets/Synthetic/Small 36-264', 4)
    # models = []
    # for i in range(4):
    #     models.append(PairwiseModel(data,i,'1','Synthetic/Small 36-264','Small_36-264'))
    # for model in models:
    #     model.trainNetwork(7000,printLoss=False)
    #     model.testNetworkValidation()
    #     current = time.time()
    #     print(f'Total time in minutes: {(current-start)/60}')

    printModelData = PairwiseYeastData('Yeast Resources/Datasets/Synthetic/Medium 36-264',4)
    printModelData.calculateCorrelations()
    # printModel = PairwiseModel(printModelData,0,'1','Synthetic/Medium 36-264','PrintTest')
    # printModel.trainNetwork(10000,printLoss=True,printTensors=True)
    # printModel.testNetworkValidation(save=False)
    

if __name__ == '__main__':
    main()