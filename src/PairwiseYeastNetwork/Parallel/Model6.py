import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test
from ComplexModel import ComplexModel
import torch

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    # complexModel = ComplexModel(int(sys.argv[1]),4,'20','Spell/Complex','Test')
    complexModel = ComplexModel(0,4,sys.argv[1],'Spell/Complex','Complex',foldFile='./Yeast Resources/Datasets/All Spell/complexGeneFolds1.csv')
    complexModel.trainNetwork(epochs=10,printLoss=True)
    complexModel.testNetworkValidation(limitNegative=True,negProportion=10,posProportion=50)
    complexModel.testNetworkTraining(limitNegative=True,negProportion=10,posProportion=50)

if __name__ == '__main__':
    main()