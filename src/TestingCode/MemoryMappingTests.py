import numpy as np
from tempfile import mkdtemp
import os.path as path


memArr = np.memmap('../YeastDict.dat',dtype=np.float32,shape=(430, 21690990),mode='r+')
np.save('../YeastDict_float16.npy',memArr.astype(np.float16))

