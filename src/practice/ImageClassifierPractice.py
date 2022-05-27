from unittest import TestLoader
import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


#To prevent freezing, all of the training needs to happen in a main method
def main():
    #Step 1: Load and Normalize Data
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))]
    )

    batch_size = 4

    #Creating training set: root specifies where training set is saved, train determines if training set, download idk, transform requires a function that determines how input features are normalized
    trainset = torchvision.datasets.CIFAR10(root='./data',train=True,download=True,transform=transform)

    #Creating trainloader: must pass in training set, batchsize, whether you want the set to be shuffled or not, and the number of workers
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,shuffle=True,num_workers=2)

    testset = torchvision.datasets.CIFAR10(root='./data',train=False,download=True,transform=transform)

    testloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,shuffle=False,num_workers=2)

    #Creating tuple of classes of objects
    classes = ('plane','car','bird','cat','deer','dog','frog','horse','ship','truck')

    def imshow(img):
        img = img / 2 + 0.5 #unormalize
        npimg = img.numpy()
        plt.imshow(np.transpose(npimg, (1,2,0)))
        plt.show()

    #Get some random training images
    dataiter = iter(trainloader)
    images, labels = dataiter.next()

    #Show images
    imshow(torchvision.utils.make_grid(images))

    #Print Labels
    print(' '.join(f'{classes[labels[j]]:52}' for j in range(batch_size)))

    #Step 2: Define a Convolutional Neural Network

    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3,6,5)
            self.pool = nn.MaxPool2d(2,2)
            self.conv2 = nn.Conv2d(6,16,5)
            self.fc1 = nn.Linear(16 * 5 * 5,120)
            self.fc2 = nn.Linear(120,84)
            self.fc3 = nn.Linear(84,10)
        
        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            x = torch.flatten(x,1) #flattens all dimensions
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x
    
    net = Net()

    #Step 3: Defining Loss Function and Optimizer
    criterion = nn.CrossEntroyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    #Step 4: Train the Network
    for epoch in range(2):
        running_loss = 0.0
        for i, data in enumerate(trainloader):
            #get the imputs; data is a lsit of [inputs,labels]
            inputs, labels = data

            #Zero the parameter gradients
            optimizer.zero_grad()

            # forwards + backwards + optimze
            outputs = net(inputs)
            loss = criterion(outputs,labels)
            loss.backwards()
            optimizer.step()

            #print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:
                print(f'[{epoch + 1}, {i + 1:5d}] loss : {running_loss / 2000:.3f}')
                running_loss = 0.0
    print('Finished Training')

    PATH = './cifar_net.pth'
    torch.svae(net.state_dict(), PATH)

    #Step 5: Testing the Network
    

    

#This should solve the freezing problem
if __name__ == '__main__':
    main()





