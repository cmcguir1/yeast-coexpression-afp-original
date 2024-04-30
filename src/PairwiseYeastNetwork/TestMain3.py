import numpy as np
import threading
import pandas as pd
import sys

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    

    data = pd.read_csv('AllGenes.csv').values
    genes = {row[0] for row in data}
    
    pairs = makePairs(genes,genes)
    memMapLen = len(pairs) - 100
    
    memMap = np.memmap(f'{sys.argv[1]}TestMemMap_Scores.dat',dtype='float16',shape=(memMapLen+100,80),mode='w+')
    

    threads  = []
    for i in range(16):
        t = threading.Thread(target=addToMemMap_Scores,args=(memMapLen))
        t.start()
        threads.append(t)
    
    print('Threads started')
    for t in threads:
        t.join()

    mismatches = []
    memMap = np.memmap(f'{sys.argv[1]}TestMemMap_Scores.dat',dtype='float16',shape=(memMapLen+100,80),mode='r+')

    for i in range(0,memMapLen):
        print(i)
        row = memMap[i]
        for j in range(80):
            if row[j] != i*j:
                mismatches.append([i*j,row[j]])
                
    pd.DataFrame(mismatches,columns=['Expected','MemMap']).to_csv(f'{sys.argv[1]}_Scores_Mismatches.csv',index=False)


    
    

    


    
def makePairs(genes1,genes2):
    pairs = []
    for geneA in genes1:
        for geneB in genes2:
            if geneA != geneB:
                pairs.append([geneA,geneB])
    return pairs



def addToMemMap_Scores(memMapLen):
    memMap = np.memmap(f'{sys.argv[1]}TestMemMap_Scores.dat',dtype='float16',shape=(memMapLen+100,80),mode='r+')

    batch = 100
    for i in range(0,memMapLen):
        memMap[i:i+batch,:] = np.array([i*j for j in range(80)],dtype='float16')
            








if __name__ == '__main__':
    main()

