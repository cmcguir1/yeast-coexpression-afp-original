from PairwiseYeastData import PairwiseYeastData
from PairwiseModel import PairwiseModel
import numpy as np

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    data = PairwiseYeastData('./Yeast Resources/Datasets/Synthetic', 4)
    model = PairwiseModel(data,0,'20x20x1','Synthetic','Test')
    model.trainNetwork(1000,printLoss=True)
    model.testNetworkValidation()
    

if __name__ == '__main__':
    main()