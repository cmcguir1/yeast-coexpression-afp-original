import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    for i in range(4):
        test(i,f'StructureTest',folderName='Spell/Structure',foldFile=f'./Yeast Resources/Datasets/All Spell/GeneFolds3.csv',structure=sys.argv[1])
        # test(0,f'TestStructure',folderName='Spell/Structure',foldFile=f'./Yeast Resources/Datasets/All Spell/GeneFolds3.csv',structure=sys.argv[1],epoch=100,datasets=5)


if __name__ == '__main__':
    main()