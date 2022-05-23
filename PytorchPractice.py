import torch
import numpy as np

a = np.array([[20,30],[12,34]])
t = torch.from_numpy(a)

shape = (2,3,)
tensor1 = torch.rand(shape)
tensor2 = torch.rand(shape)
tensor3 = torch.zeros(shape)
tensor4 = torch.ones(shape)

print(tensor1)
print(tensor3)
print(tensor1 * tensor3)
print(tensor1 * tensor4)
print(tensor1 * tensor2)