import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    test(0,'Spell_lr0.005',lr=0.005)
    #test(0,'ModelTest2',batch_size=20,epoch=1000,datasets=10)

if __name__ == '__main__':
    main()