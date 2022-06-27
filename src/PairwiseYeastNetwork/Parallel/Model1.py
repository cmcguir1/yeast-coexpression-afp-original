import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    for i in range(4):
        test(i,'DNARepair',posGenes='./Yeast Resources/GeneSets/GO0006302_Pos.txt',negGenes='./Yeast Resources\GeneSets\GO0006302_Neg.txt',foldFile='./Yeast Resources/GeneSets/GO0006302Folds1.csv',folderName='Spell/OtherGOTerms')
    # test(0,'TestDNARepair',posGenes='./Yeast Resources/GeneSets/GO0006302_Pos.txt',negGenes='./Yeast Resources\GeneSets\GO0006302_Neg.txt',foldFile='./Yeast Resources/GeneSets/GO0006302Folds1.csv',folderName='Spell/OtherGOTerms',epoch=1000,datasets=10)

if __name__ == '__main__':
    main()