import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class FocalLoss(nn.Module):
    def __init__(self,alpha=1,gamma=1,weight=None, size_average=True):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.sm = torch.nn.Softmax(dim=1)

    def forward(self, inputs, targets,smooth=1):
        
        #comment out if your model contains a sigmoid or equivalent activation layer
        #inputs = self.sm(inputs)
        inputs = torch.sigmoid(inputs)       
        
        #flatten label and prediction tensors
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        
        #first compute binary cross-entropy 
        #BCE = F.binary_cross_entropy(inputs, targets, reduction='mean')
        BCE = F.binary_cross_entropy(inputs, targets, reduction='none')
        BCE_EXP = torch.exp(-BCE)
        focal_loss = self.alpha * ((1-BCE_EXP)**self.gamma) * BCE
        focal_loss = torch.mean(focal_loss)
                       
        return focal_loss

