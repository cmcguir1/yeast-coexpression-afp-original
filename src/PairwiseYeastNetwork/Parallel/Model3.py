import sys
sys.path.insert(0,'./src/PairwiseYeastNetwork')
from ModelTester import test

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    test(int(sys.argv[1]),f'Spell_batch{sys.argv[2]}',batch_size=int(sys.argv[2]),folderName='Spell/BatchTests')
    # test(0,f'TestSpell_batch{12}',batch_size=12,folderName='Spell/BatchTests',epoch=100,datasets=10)

if __name__ == '__main__':
    main()