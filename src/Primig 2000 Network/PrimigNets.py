import torch
import torch.nn as nn
import torch.nn.functional as F

#Flexible Network class that constructs a neural network based on a specified structure
#I refactored this class to use sequential instead of a list of layers
class PrimegNet(nn.Module):
    def __init__(self,structure):
        super().__init__()
        self.structure = structure
        #Makes a list of sizes of each network layer, then intializes a list to hold these layers
        sizes = self.structure.split('x')
        # self.layers = []
        self.layers = nn.Sequential()
        #Loop that adds each layer to the layers list
        for i in range(len(sizes)-1):
            #Adds a new layer
            self.layers.add_module(f'Layer {i + 1}',nn.Linear(int(sizes[i]),int(sizes[i+1])))
            #Performs a ReLU after that layer, unless it is the final layer before the output nodes
            if(i == len(sizes) - 2):
                self.layers.add_module(f'ReLU',nn.ReLU())

            # self.layers.append(nn.parameter.Parameter(nn.Linear(int(sizes[i]),int(sizes[i+1]))))

    def forward(self,x):
        #This loop feed forwards the input each layer, then applies the relu activation function
        #This loop does not feed forward to the output layer because no relu is used
            # for i in range(len(self.layers)-1):
            #     x = F.relu(self.layers[i](x))
        #Feeds last hidden layer output to output layer
            # x = self.layers[-1](x)


        #Applies sequential function
        x = self.layers(x)
        #You need to squish with a sigmoid because Binary Cross Entropy needs to output values to be normalized between 0 and 1
        x = torch.sigmoid(x)
        return x
