import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test
from ComplexModel import ComplexModel

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    complexModel = ComplexModel(int(sys.argv[1]),4,'20','Spell/Complex','Test')
    complexModel.trainNetwork(20000,printLoss=True)

if __name__ == '__main__':
    main()