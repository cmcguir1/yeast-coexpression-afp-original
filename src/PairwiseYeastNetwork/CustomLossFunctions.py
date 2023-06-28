import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

# Focal Loss is a a version of cross entropy that upweights the loss of training examples that do poorly
class FocalLoss(nn.Module):
    def __init__(self,alpha=None,gamma=1,nonSpecific=False):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.nonSpecific = nonSpecific
        

    def forward(self, inputs, targets,smooth=1):
        
        
        if self.nonSpecific:

            end = len(inputs[0]) - 1
            
            CE = F.cross_entropy(inputs[:,:end],targets[:,:end],reduction='none',weight=self.alpha)
            pt = torch.exp(-CE)
            fl = torch.mean(((1-pt)**self.gamma) * CE) + F.binary_cross_entropy_with_logits(inputs[:,end],targets[:,end])
        #first compute binary cross-entropy 
        else:
            CE = F.cross_entropy(inputs,targets,reduction='none',weight=self.alpha)
            pt = torch.exp(-CE)
            fl = torch.mean(((1-pt)**self.gamma) * CE)
        
        return fl
    
# Version of Mean Squared Error that first takes the softmax of the output vector
class SM_MSE(nn.Module):
    def __init__(self):
        super(SM_MSE, self).__init__()
        self.sm = nn.Softmax(dim=1)
        

    def forward(self, inputs, targets):
        return F.mse_loss(self.sm(inputs),target=targets)

# Version of Binary Cross Entropy that takes the softmax of the output vector instead of the sigmoid   
class SM_BCE(nn.Module):
    def __init__(self):
        super(SM_BCE, self).__init__()
        self.sm = nn.Softmax(dim=1)
        

    def forward(self, inputs, targets):
        return F.binary_cross_entropy(self.sm(inputs),target=targets)
    
# Version of Cross Entropy that allows for calculating the loss of non-specific node as a seperate binary cross entropy
class CustomCrossEntropyLoss(nn.Module):
    def __init__(self,alpha=None,nonSpecific=False):
        super(CustomCrossEntropyLoss, self).__init__()
        self.alpha = alpha
        self.noneSpecific = nonSpecific
        

    def forward(self, inputs, targets):
        
        
        if self.noneSpecific:
            end = len(inputs[0]) - 1
            CE = F.cross_entropy(inputs[:,:end],targets[:,:end],reduction='mean',weight=self.alpha) + F.binary_cross_entropy_with_logits(inputs[:,end],targets[:,end])
        #first compute binary cross-entropy 
        else:
            CE = F.cross_entropy(inputs,targets,reduction='mean',weight=self.alpha)
            
        
        return CE
    
class ComboCrossEntropy(nn.Module):
    def __init__(self):
        super(ComboCrossEntropy,self).__init__()
        self.sm = torch.nn.Softmax(dim=1)

    def forward(self,inputs,targets):
        loss = F.cross_entropy(inputs,targets,reduction='mean') + F.mse_loss(self.sm(inputs),targets)
        return loss
    

    


