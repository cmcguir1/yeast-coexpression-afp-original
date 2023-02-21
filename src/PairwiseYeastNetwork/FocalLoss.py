import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

class FocalLoss(nn.Module):
    def __init__(self,weights,gamma=2):
        super(FocalLoss,self).__init__()
        self.alpha = weights
        self.gamma = gamma
    
    def forward(self,outputs,labels):
        outputs = torch.sigmoid(outputs)
        outputs = outputs.view(-1)
        labels = labels.view(-1)

        BCE = F.binary_cross_entropy(outputs,labels,reduction='mean')


        BCE_EXP = torch.exp(-BCE)
        focalLoss = torch.mean(self.alpha * (1-BCE_EXP)**self.gamma * BCE)

        return focalLoss
