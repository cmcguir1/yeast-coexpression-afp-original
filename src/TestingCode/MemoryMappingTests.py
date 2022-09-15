import numpy as np
from tempfile import mkdtemp
import os.path as path

numRows = 10
numCols = 10
memArr = np.memmap('./memmapExample.dat',dtype=np.float32,shape=(numRows,numCols),mode='w+')
for i in range(numRows):
    for j in range(numCols):
        memArr[i,j] = i* j * 0.5

memArr = np.memmap('./memmapExample.dat',dtype=np.float32,shape=(numRows,numCols),mode='r')
print(memArr)
