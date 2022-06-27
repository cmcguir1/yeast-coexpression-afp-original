import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    for i in range(4):
        test(i,f'FoldsTest{sys.argv[1]}',folderName='Spell/FoldsTest',foldFile=f'./Yeast Resources/Datasets/All Spell/GeneFolds{sys.argv[1]}.csv')
    # test(0,f'TestFoldsTest{1}',folderName='Spell/FoldsTest',foldFile=f'./Yeast Resources/Datasets/All Spell/GeneFolds{2}.csv',epoch=100,datasets=10)

if __name__ == '__main__':
    main()