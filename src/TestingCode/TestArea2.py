import pandas as pd
import torch

outputs = torch.tensor([[1000,1,10,1,1]],dtype=torch.float32)
labels = torch.tensor([[1,0,1,0,0]],dtype=torch.float32)
weights = torch.tensor([10,1,1,1,1],dtype=torch.float32)

loss = torch.nn.CrossEntropyLoss()
weightedLoss = torch.nn.CrossEntropyLoss(weight=weights)

print(f'Loss: {loss(outputs,labels)}')
print(f'Weighted Loss: {weightedLoss(outputs,labels)}')