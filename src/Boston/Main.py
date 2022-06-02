import torch
from BostonData import BostonData

#This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    #Ask Hibbs if I should normalize my outputs in the dataset
    data = BostonData(4)
    trainingData, validationData = data.getFoldDatasets(0)
    print(trainingData[0])
    for f, l in trainingData:
        print
        print(f)
        print(l)
        

if __name__ == '__main__':
    main()