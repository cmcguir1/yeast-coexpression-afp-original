import torch
import torch.nn as nn
import torch.nn.functional as F

#Flexible Network class that constructs a neural network based on a specified structure
class FlexNet(nn.Module):
    def __init__(self,structure,activation='relu',sigmoid=True,inputDrop=None,hiddenDrop=None):
        super().__init__()
        self.structure = structure
        #Makes a list of sizes of each network layer, then intializes a list to hold these layers
        sizes = self.structure.split('x')
        #Variable to control if sigmoid is applied to the last hidden laeyer
        self.sigmoid = sigmoid
        # self.layers = []
        self.layers = nn.Sequential()

        if(inputDrop == None):
            self.dropInput = nn.Dropout(p=0.0)
        else:
            self.dropInput = nn.Dropout(p=inputDrop)
        if(hiddenDrop == None):
            self.dropHidden = nn.Dropout(p=0.0)
        else:
            self.dropHidden = nn.Dropout(p=hiddenDrop)

        #Conditional to determine activation function of network
        if(activation == 'relu'):
            self.activation = nn.ReLU()
        elif(activation == 'tanh'):
            self.activation = nn.Tanh()
        elif(activation == 'sigmoid'):
            self.activation = nn.Sigmoid()
        else:
            self.activation = nn.LeakyReLU()

        #If input dropout is specified, add dropout as first layer
        if(inputDrop != None):
            self.layers.add_module('Input Dropout',self.dropInput)

        #Loop that adds each layer to the layers list
        for i in range(len(sizes)-1):
            #Adds a new layer
            self.layers.add_module(f'Layer {i + 1}',nn.Linear(int(sizes[i]),int(sizes[i+1])))
            #Performs a ReLU after that layer, unless it is the final layer before the output nodes
            if(i != len(sizes) - 2):
                self.layers.add_module(f'ReLU',self.activation)
                if(hiddenDrop != None):
                    self.layers.add_module('Hidden Layer Dropout',self.dropHidden)

            # self.layers.append(nn.parameter.Parameter(nn.Linear(int(sizes[i]),int(sizes[i+1]))))

    def forward(self,x,test=False):
        #If testing, change the dropout layers to not dropout
        if(not(test)):
            self.dropHidden = nn.Dropout(p=0.0)
            self.dropInput = nn.Dropout(p=0.0)

        #Applies sequential function
        x = self.layers(x)
        #You need to squish with a sigmoid because Binary Cross Entropy needs to output values to be normalized between 0 and 1
        if(self.sigmoid):
            x = torch.sigmoid(x)
        return x