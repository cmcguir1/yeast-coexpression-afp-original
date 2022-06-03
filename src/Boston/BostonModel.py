import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.optim as optim
import BostonNetworks as BN

class BostonModel():
    def __init__(self,trainingData,valData,networkType,batch_size=4,lr=0.01,momentum=0.9):
        #Initializes a training loader and a validation loader from passed in datasets
        self.batch_size = batch_size
        self.trainloader = DataLoader(trainingData,batch_size=self.batch_size,shuffle=True,num_workers=2)
        self.valLoader = DataLoader(valData,batch_size=self.batch_size,shuffle=True,num_workers=2)
        
        #Conditional that chooses a network based on which string you pass in
        if(networkType == '13x3x1'):
            self.net = BN.BostonNet1()
        elif(networkType == '13x5x1'):
            self.net = BN.BostonNet2()
        else:
            self.net = BN.BostonNet3()
        
        #Check if CUDA is available, then pass net to available device
        self.device = torch.device('cuda:0' if (torch.cuda.is_available()) else 'cpu')
        self.net.to(self.device)
        
        #Define a loss function and an optimizer
        self.lossFunc = nn.MSELoss()
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)

    def trainNetwork(self,epochs,printLoss=False):
        #Loops over the number of epochs
        running_loss = 0.0
        for epoch in range(epochs):
            #Loops over training data set
            running_loss = 0.0
            for batch, data in enumerate(self.trainloader):
                #Zero gradient before each batch loop
                self.opt.zero_grad()

                #Divides features and labels from each batch, then sends both tensors to device
                features, labels = data[0].to(self.device), data[1].to(self.device)

                #Feeds forward, calculates loss, backpropagates, then updates weights
                outputs = self.net(features)
                loss = self.lossFunc(outputs.float(),labels.float()) #For some reason, outputs and laebls were of the type double and needed to be floats
                running_loss += loss
                loss.backward()
                self.opt.step()

                #Prints out the loss if printLoss is true
                if((batch + 1) % (len(self.trainloader) / 5) == 0 and printLoss):
                    print(f'Epoch: {epoch} Loss: {running_loss}')
                    running_loss = 0.0

    
    #Helper function to denormalize ouput data for the time being
    def denorm(x):
        mean = 22.532806324110698
        x = (2 ** x) * mean
        return x
    
    def testNetwork(self,dataloader):
        #Variables to keep track of average error over all testing examples
        total = 0.0
        averageError = 0.0
        
        #Torch environment where gradients are not calculated
        with torch.no_grad():
            #Loops over all data in data loader
            for batch, data in enumerate(dataloader,0):
                features, labels, = data[0].to(self.device), data[1].to(self.device)
                outputs = self.net(features)
                #Calculates percent error for all outputs
                for i in range(len(outputs)):
                    averageError += abs((BostonModel.denorm(outputs[i])-BostonModel.denorm(labels[i]))/BostonModel.denorm(labels[i]))
                total += len(outputs)
        
        return (averageError.item()/total)*100

    #Calls testNetwork with training data
    def testNetworkTrain(self):
        return self.testNetwork(self.trainloader)

    #Call testNetwork with validation data
    def testNetworkVal(self):
        return self.testNetwork(self.valLoader)

    #Saves Model's network to Saved Networks folder
    def saveNetwork(self):
        path = input('Name of file: ')
        self.net._save_to_state_dict(f'./Saved Networks/{path}')

    
        
                
