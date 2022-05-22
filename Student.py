from re import I, X


class Student:


    def __init__(self,n,g,id) -> None:
        self.name = n
        self.gpa = g
        self.idNumber = id
        self.x = "Attribute"
    
    def giveInformation(self):
        return self.name + self.x

    

    