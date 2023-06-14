import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class FocalLoss(nn.Module):
    def __init__(self,alpha=None,gamma=1,nonSpecific=False):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.noneSpecific = nonSpecific
        

    def forward(self, inputs, targets,smooth=1):
        
        
        if self.noneSpecific:

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
    


