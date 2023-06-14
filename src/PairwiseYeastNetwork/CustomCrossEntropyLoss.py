import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

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
    


