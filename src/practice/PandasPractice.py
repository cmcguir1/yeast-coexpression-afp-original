import pandas as pd
import numpy as np
import torch

file = pd.read_csv('resources/IRIS.csv')
print(file)

randomized = file.sample(frac=1)
print(randomized)

#data = randomized.to_numpy()[:,4]

x = randomized.to_numpy()
print(x)

y = np.delete(x,4,1)
print(y)

z = torch.from_numpy(y.astype('float32'))
print(z)



