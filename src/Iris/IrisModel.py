from cProfile import label
import enum
from pyexpat import features
from unittest import TestLoader
from sqlalchemy import null
import torch
import torch.optim as optim
from IrisNetworks import IrisNet4x3
import IrisData

#Model is a class that holds everything need to test a neural network
class IrisModel():
    def __init__(self,dataset,network=IrisNet4x3(),lr=0.001,momentum=0.9,bs=4):
        #Intializes train and test loaders from the passed in IrisData
        self.trainloader = torch.utils.data.DataLoader(dataset.trainingData,batch_size=bs,shuffle=True,num_workers=2)
        self.testloader = torch.utils.data.DataLoader(dataset.testingData,batch_size=bs,shuffle=True,num_workers=2)
        
        #Checks if CUDA is available, if so, moves net to gpu
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.net = network
        self.net.to(self.device)

        #Intialize loss function and optimizer
        self.lossFunc = torch.nn.CrossEntropyLoss()
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)

    def trainNetwork(self,epochs):
        #Loop over the training set a specified epochs number of times
        for epoch in range(epochs):
            #Loop over training set
            running_loss = 0.0
            #Looop over training set, enumerate returns an iterator of the count and value of trainloader
            for i, loopData in enumerate(self.trainloader,0):
                #Gets features and labels from trainloader, then moves them to gpu
                features = loopData[0].to(self.device)
                labels = loopData[1].to(self.device)

                #Zeros out gradient before next feedforward
                self.opt.zero_grad()
                
                #Feeds Forward, then calculates loss of that output
                outputs = self.net(features)
                loss = self.lossFunc(outputs,labels)

                #Adds loss of this feed forward to running loss, we use .item() because loss is a tensor (I think)
                running_loss += loss.item()

                #Calculate gradients, then adjust weights
                loss.backward()
                self.opt.step()

                #Prints total loss to the screen 4 times per loop through the dataset
                if(i % int(len(self.trainloader)/4) == 0):
                    print(f'Epoch: {epoch + 1} Batches: {i + 1:5d} Running Loss: {running_loss:3f}')
                    running_loss = 0.0
                
        print('Finished Training')

    def testNetworkAccuracy(self,dataLoader):
        correct = 0
        total = 0
        #Context manager that disables the calculaation of gradients to conserve memory
        with torch.no_grad():
            #Loop over all the data in the dataLoader
            for i, loopData in enumerate(dataLoader,0):
                features, labels = loopData[0].to(self.device), loopData[1].to(self.device)
                outputs = self.net(features)

                #predictions stores the index number of maximum value from each output vector
                _, predictions = torch.max(outputs,1)

                #calls max on labels to match its format to predictions
                _, labels = torch.max(labels,1)

                #Adds the number of predictions in each batch to total predictions
                total += predictions.size(0)
                #Does element wise comparison to see how many predictions from batch were correct
                correct += (predictions == labels).sum().item() #(tensor == tensor) returns a tensor of booleans where each boolean determines if the values of each tensor match in that position
        print(f'Accuracy: {(correct / total)*100:.3f}%')
                




    def testNetworkAccuracyTraining(self):
        self.testNetworkAccuracy(self.trainloader)

    def testNetworkAccuracyTesting(self):
        self.testNetworkAccuracy(self.testloader)

    def saveModelNetwork(self,pathName):
        pass

    def loadModelNetwork(self,pathName):
        pass
    
                


