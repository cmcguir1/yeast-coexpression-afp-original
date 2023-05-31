import torch
import numpy as np
from FocalLoss import FocalLoss

import sys
sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

print(len(getGenes('GO:0032543',dataset='original')))
print(len(getGenes('GO:0007005',dataset='original')))
print(len(set(getGenes('GO:0032543',dataset='original'))&set(getGenes('GO:0007005',dataset='original'))))

# ce = torch.nn.CrossEntropyLoss(reduction='none')
# fl = FocalLoss(alpha=1,gamma=0)
# lsm = torch.nn.LogSoftmax(dim=1)

# output = torch.tensor([[10,1,10,1,2]],dtype=torch.float)
# labels = torch.tensor([[1,0,1,0,0]],dtype=torch.float)
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

