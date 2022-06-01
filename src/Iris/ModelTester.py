import torch
from Iris.IrisNetworks import IrisNet4x3
from IrisData import IrisData

class ModelTester():
    def __init__(self,structure,dataPath= './resources/IRIS.csv'):
        self.structure = structure