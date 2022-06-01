from cProfile import label
import enum
from pyexpat import features
from unittest import TestLoader
from sqlalchemy import null
import torch
import torch.optim as optim
from IrisNetworks import IrisNet4x3
from IrisData import IrisData

#Model is a class that holds everything need to test a neural network
class IrisModel():
    def __init__(self,filePath,network=IrisNet4x3(),lr=0.001,momentum=0.9,bs=4):
        #Save filePath as a field
        self.dataPath = filePath

        #intialize data for model, this data should be randomized and stratified
        self.data = IrisData(0.7,self.dataPath)

        #Intializes train and test loaders from the passed in IrisData
        self.trainloader = torch.utils.data.DataLoader(self.data.trainingData,batch_size=bs,shuffle=True,num_workers=2)
        self.testloader = torch.utils.data.DataLoader(self.data.testingData,batch_size=bs,shuffle=True,num_workers=2)
        
        #Checks if CUDA is available, if so, moves net to gpu
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.net = network
        self.net.to(self.device)

        #Intialize loss function and optimizer
        self.lossFunc = torch.nn.CrossEntropyLoss()
        self.opt = optim.SGD(self.net.parameters(),lr=lr,momentum=momentum)

    #Resets network with new randomized data and an untrained newtwork
    # def resetModel(self):
    #     self.data = IrisData(0.7)
    #     self.trainloader = torch.utils.data.DataLoader(self.data.trainingData,batch_size=bs,shuffle=True,num_workers=2)
    #     self.testloader = torch.utils.data.DataLoader(self.data.testingData,batch_size=bs,shuffle=True,num_workers=2)
    #     #This method should reset all of the weights and biases of each layer of the net, but I a
    #     for para in self.net.children():
    #         if(hasattr(para,'reset_parameters')):
    #             para.reset_parameter()

    def trainNetwork(self,epochs,shouldPrint=False):
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
                if(i % int(len(self.trainloader)/4) == 0 and shouldPrint):
                    print(f'Epoch: {epoch + 1} Batches: {i + 1:5d} Running Loss: {running_loss:3f}')
                    running_loss = 0.0
                
        print('Finished Training')

    def testNetworkAccuracy(self,dataLoader,title):
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
        print(f'{title} Accuracy: {(correct / total)*100:.3f}%')
                
    #Tests the model's accuracy on data it was trained with
    def testNetworkAccuracyTraining(self):
        self.testNetworkAccuracy(self.trainloader,'Training Data')

    #Tests the model's accuracy on data it has not seen before
    def testNetworkAccuracyTesting(self):
        self.testNetworkAccuracy(self.testloader, 'Testing Data')

    def saveModelNetwork(self,pathName):
        pass

    def loadModelNetwork(self,pathName):
        pass
    
                


