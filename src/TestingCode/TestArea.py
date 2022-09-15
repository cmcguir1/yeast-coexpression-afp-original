import string
from tokenize import String
import numpy as np

lst = [1,2,3,np.nan,5]
lst2 = ["Hello","What","Cole"]
arr = np.array(lst2,dtype='<U5')

print(arr)
print(arr.dtype)