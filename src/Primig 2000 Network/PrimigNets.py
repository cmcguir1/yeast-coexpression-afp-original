import torch.nn as nn
import torch.nn.functional as F

#Flexible Network class that constructs a neural network based on a specified structure
class PrimegNet(nn.Module):
    def __init__(self,structure):
        super().__init__()
        self.structure = structure
        #Makes a list of sizes of each network layer, then intializes a list to hold these layers
        sizes = self.structure.split('x')
        self.layers = []
        #Loop that adds each layer to the layers list
        for i in range(len(sizes)-1):
            self.layers.append(nn.Linear(int(sizes[i]),int(sizes[i+1])))

    def forward(self,x):
        #This loop feed forwards the input each layer, then applies the relu activation function
        #This loop does not feed forward to the output layer because no relu is used
        for i in range(len(self.layers)-1):
            x = F.relu(self.layers[i](x))
        #Feeds last hidden layer output to output layer
        x = self.layers[-1](x)
        return x
