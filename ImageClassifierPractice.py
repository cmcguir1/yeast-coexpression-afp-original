from unittest import TestLoader
import torch
import torchvision
import torchvision.transforms as transforms

#Step 1: Load and Normalize Data

#

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



