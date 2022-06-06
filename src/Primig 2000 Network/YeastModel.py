import torch
from YeastData import YeastData
from PrimigNets import PrimegNet
import torch.nn as nn
import torch.optim as optim


class YeastModel():
    def __init__(self,structure,lr,momentum):
        self.data = YeastData(.2,4)
        self.trainLoader = None
        self.valLoader = None
        
        self.net = PrimegNet(structure)
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.net.to(self.device)

        self.lossFunc = nn.CrossEntropyLoss()
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)