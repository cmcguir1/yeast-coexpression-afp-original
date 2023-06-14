import torch
import numpy as np
from FocalLoss import FocalLoss
from CustomCrossEntropyLoss import CustomCrossEntropyLoss
import torch.nn.functional as F

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

print(torch.tensor([[0],[1],[1]]).size())
# ce = torch.nn.CrossEntropyLoss()
# c_ce = CustomCrossEntropyLoss()
# fl = FocalLoss(alpha=torch.tensor([1,1,1,1]),gamma=0,nonSpecific=True)


# output = torch.tensor([[10,1,10,1,2]],dtype=torch.float)
# labels = torch.tensor([[1,0,1,0,0]],dtype=torch.float)

# print(f'Cross Entropy: {ce(output,labels)}')
# print(f'Focal Loss: {fl(output,labels)}')
# print(f'Custom Cross Entropy: {c_ce(output,labels)}')



# soft = F.softmax(output.view(-1),dim=-1)
# print(soft)
# ce_loss = F.nll_loss(soft,labels.view(-1).type(torch.LongTensor),reduction='mean')
# print(labels.view(-1))
# ce_loss = -1 * torch.sum(torch.log(soft))


# print(f'Cross Entropy Loss: {CE(output,labels).item()}')
# print(f'Functional ce: {F.cross_entropy(output,labels,reduction="none")}')
# print(f'My ce: {ce_loss}')
# print(f'CE: {ce(output,labels)}')
# print(f'FL: {fl(output,labels)}')
# print(torch.nn.functional.binary_cross_entropy(torch.sigmoid(output),labels,reduction='none'))
# print(ce(output,labels))
# print(lsm(output).view(lsm(output).size(0),-1))
# print(labels.view(labels.size(0),-1))
# print(torch.nn.functional.nll_loss(lsm(output).view(lsm(output).size(0),-1),labels.view(labels.size(0),-1)))
# print(torch.nn.functional.cross_entropy(output,labels,reduction='sum'))
# print(torch.nn.functional.cross_entropy(output,labels,reduction='mean'))
# print(torch.nn.functional.cross_entropy(output,labels,reduction='none'))

