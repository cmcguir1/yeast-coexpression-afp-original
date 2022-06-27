import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    for i in range(4):
        test(i,f'VariabilityTest{sys.argv[1]}',folderName='Spell/VariabilityTest')
    # test(0,f'TestVariabilityTest{1}',folderName='Spell/VariabilityTest',epoch=100,datasets=10)

if __name__ == '__main__':
    main()