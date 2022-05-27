from cProfile import label
from unittest import TestLoader
from sklearn import neural_network
import torch
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    #Step 1: Load and normalize the data
    #We first intialize our transform function that will normalize our image data
    transform = transforms.Compose( #Compose combines multiple transforms together
        [transforms.ToTensor(), #ToTensor() converts PIL image to tensor of
        transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))] # Normalize takes in a tuple of means and a tuple standard deviations
    )
    batch_size = 4

    trainset = torchvision.datasets.CIFAR10(root='./data',train=True,download=True,transform=transform)
    #Created a Dataloader for trainset, which is an sequence of size 4 minibatches which are shuffled, and 2 workers
    trainloader = torch.utils.data.DataLoader(trainset,batch_size=batch_size,shuffle=True,num_workers=2)

    testset = torchvision.datasets.CIFAR10(root='./data',train=False,download=True,transform=transform)
    testloader = torch.utils.data.DataLoader(testset,batch_size=batch_size,shuffle=True,num_workers=2)

    #initializing a tuple of labels for the outputs
    classes = ('plane','car','bird','cat','deer','dog','frog','horse','ship','truck')

    #This section will display some of the image from trainloader
    def imshow(img):
        img = img / 2 + 0.5 # unnormalize
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg,(1,2,0)))
        plt.show()

    dataiter = iter(trainloader)
    images, labels = dataiter.next()

    #imshow(torchvision.utils.make_grid(images))
    print(' '.join(f'{classes[labels[j]]:5s}' for j in range(batch_size)))

    #Step 2: Defining a Convolutional Neural Network

    #Creating a neural network class that extends Module, we will need to define an __inti__ and forward method
    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            #These first 3 lines define to convolutional layers and a maxpool activation function
            self.conv1 = nn.Conv2d(3,6,5)
            self.pool = nn.MaxPool2d(2,2)
            self.conv2 = nn.Conv2d(6,16,5)
            #The ouput of the conv2 layer is flattened, then passed to a linear layer with 120 outputs
            self.fc1 = nn.Linear(16 * 5 * 5, 120)
            self.fc2 = nn.Linear(120,84)
            #The last linear layer has 10 output nodes, representing each of our 10 labels
            self.fc3 = nn.Linear(84,10)
        
        def forward(self,x):
            #These first two steps pass the input x through the conv layers and apply the maxpool activation function to them
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            #The output of the conv layers is flattened so that it can be passed into a linear layer
            x = torch.flatten(x,1)
            #These next two layers pass the flattened tensor through two linear layers with relu activaiton functions
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            #The last layer produces ouptut tensor
            x = self.fc3(x)
            return x

        def forwardPrintDims(self,x):
            print('Input Layer: ' + str(x.shape))
            #These first two steps pass the input x through the conv layers and apply the maxpool activation function to them
            x = self.pool(F.relu(self.conv1(x)))
            print('Hidden Layer 1 (Conv): ' + str(x.shape))
            x = self.pool(F.relu(self.conv2(x)))
            print('Hidden Layer 2 (Conv): ' + str(x.shape))
            #The output of the conv layers is flattened so that it can be passed into a linear layer
            x = torch.flatten(x,1)
            #These next two layers pass the flattened tensor through two linear layers with relu activaiton functions
            x = F.relu(self.fc1(x))
            print('Hidden Layer 3 (Linear): ' + str(x.shape))
            x = F.relu(self.fc2(x))
            print('Hidden Layer 4 (Linear): ' + str(x.shape))
            #The last layer produces ouptut tensor
            x = self.fc3(x)
            print('Output Layer: ' + str(x.shape))

    net = Net()

    #Step 3: Defining a Loss function

    #We define criterion as our loss function, because our outputs are categorial, we choose cross entropy as our loss function
    criterion = nn.CrossEntropyLoss()

    #An optimizer will handle adjust our parameter (our weights and biasses) after we call backwards on our loss function
    #We define our optimizer as a stoichastic gradient descent optimizer as that is the only type of adjusting I know
    optimizer = optim.SGD(net.parameters(),lr=0.001, momentum=0.9)

    #Step 4: Train the network

    def trainNetwork():
        #We create our trainig loop that will run for a certain number of epochs
        for epoch in range(30):
            
            #running loss will keep track of the total loss for every 2000 minibatches
            running_loss = 0.0

            #This is the loop for 
            for i, data in enumerate(trainloader,0):
                
                #gettign the put: data is a list of [inputs, labels]
                inputs, labels = data[0].to(device), data[1].to(device)

                #Zeros out gradients of all weights before next backwards
                optimizer.zero_grad()

                #Feeding the input mini batch into the neural network and storing the output tensor in outputs
                outputs = net(inputs)
                #Calculating the loss of this mini batch
                loss = criterion(outputs,labels)
                #Backpropagates, calculates gradients of each tensor of weights
                loss.backward()
                #Optimzer adjusts weights and biases using gradients
                optimizer.step()

                #Print statistics
                running_loss += loss.item() #sums total loss of 2000 mini batches
                if i % 2000 == 1999:
                    print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
                    running_loss = 0.0

    #trainNetwork()
    #print('Finished training')
    
    #Saving neural network
    PATH = './cifar_net.pth'
    #torch.save(net.state_dict(), PATH)

    #Step 5: Testing the network
    


    #This resets the trained neural network back to a random network
    net = Net()
    #Loads in trained network
    net.load_state_dict(torch.load(PATH))

    #Moves net to GPU for faster training
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    net.to(device)
    trainNetwork()

    #makes an iterator of test data, then passes the next of that iterator throught the network
    dataiter = iter(testloader)
    images, labels
    dataTemp = dataiter.next()
    images, labels = dataTemp[0].to(device), dataTemp[1].to(device)
    outputs = net(images)

    images, labels = dataiter.next()

    testNetwork()

    #singleOutput = net.forwardPrintDims(images)

    #Displays images
    #imshow(torchvision.utils.make_grid(images))
    #print('Groundtruth: ', ' '.join(f'{classes[labels[j]]:5s}' for j in range(4)))

    #Stores max output value in predicted
    def testNetwork():
        
        _, predicted = torch.max(outputs,1)
        print(predicted)

        print('Predicted: ', ' '.join(f'{classes[predicted[j]]:5s}' for j in range(4)))

        correct = 0
        total = 0
        with torch.no_grad():
            #loops over all data in testloader
            for data in testloader:
                images, labels = data[0].to(device), data[1].to(device)
                #Feeds test images through network
                output = net(images)
                _, predicted = torch.max(outputs.data, 1) #max takes two arguments, the tensor you want to max, and the dimension of the tensor you want to max on
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        print(f'Accuracy of the network on the 10000 test images: {100 * correct // total}%')





if __name__ == '__main__':
    main()

