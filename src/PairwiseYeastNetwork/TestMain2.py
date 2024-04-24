import numpy as np
import threading
import pandas as pd

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():

    

    data = pd.read_csv('AllGenes.csv').values
    genes = {row[0] for row in data}
    
    # pairs = makePairs(genes,genes)[:100000]
    
    
    

    # threads  = []
    # for i in range(16):
    #     t = threading.Thread(target=addToMemMap,args=(pairs,))
    #     t.start()
    #     threads.append(t)
    
    # print('Threads started')
    # for t in threads:
    #     t.join()

    memMap = np.memmap('TestMemMap.dat',dtype='U10',shape=(100000,2),mode='r+')
    print(memMap.dtype)
    
    # print("Checking for errors")
    
    for [geneA, geneB] in memMap:
        print(repr(geneA),repr(geneB))
    #     if geneA not in genes:
    #         print('Not found:',geneA)
    #     if geneB not in genes:
    #         print('Not found:',geneB)

    


    
def makePairs(genes1,genes2):
    pairs = []
    for geneA in genes1:
        for geneB in genes2:
            if geneA != geneB:
                pairs.append([geneA,geneB])
    return pairs

def addToMemMap(pairs):
    
    
    
    
    memMap = np.memmap('TestMemMap.dat',dtype='U10',shape=(100000,2),mode='r+')
    
    batch = 100
    for j in range(500):
        for i in range(0,100000,batch):
            memMap[i:i+batch,:] = np.array(pairs[i:i+batch],dtype='U10')








if __name__ == '__main__':
    main()

