import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

class FocalLoss(nn.Module):
    def __init__(self,alpha=0.25,gamma=2):
        super(FocalLoss,self).__init__()
        self.alpha = alpha
        self.gamma = gamma
    
    def forward(self,outputs,labels):
        # outputs = torch.sigmoid(outputs)
        # outputs = outputs.view(-1)
        # labels = labels.view(-1)

        # BCE = F.binary_cross_entropy(outputs,labels,reduction='mean')
        # print(f'BCE: {BCE}')

        # BCE_EXP = torch.exp(-BCE)
        # print(f'BCE_EXP: {BCE_EXP}')
        # focalLoss = torch.sum(self.alpha * (1-BCE_EXP)**self.gamma * BCE)
        focalLoss = torch.sum(torchvision.ops.sigmoid_focal_loss(outputs,labels,gamma=self.gamma,alpha=self.alpha))
        #print(focalLoss)

        return focalLoss
