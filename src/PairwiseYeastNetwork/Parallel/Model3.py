import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test
from ComplexModel import ComplexModel
import torch
import time

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    start = time.time()
    # complexModel = ComplexModel(int(sys.argv[1]),4,'20','Spell/Complex','Test')
    complexModel = ComplexModel(int(sys.argv[1]),4,sys.argv[2],'Spell/ComplexTest','ComplexTest',foldFile='./Yeast Resources/Datasets/All Spell/complexGeneFolds1.csv')
    complexModel.net.load_state_dict(torch.load(f'./Yeast Resources/Pairwise/Spell/Complex/Complex_20_Net_fold{int(sys.argv[1])+1}.pth'))
    print('Began Testing on Validation')
    complexModel.testNetworkValidation(limitNegative=True,negProportion=10)
    print(f'Total Run Time: {(time.time()-start)/60} minutes')
    #complexModel.testNetworkTraining(limitNegative=True,negProportion=10)

if __name__ == '__main__':
    main()