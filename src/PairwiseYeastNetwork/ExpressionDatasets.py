import glob
import time
from YeastDataFile import YeastDataFile
import pandas as pd

class ExpressionDatasets():
    def __init__(self,numDatasets,folder,pairs,subset,sort=True,recur=True,recalc=False,statsDictLoc=''):
        #Make a dictionary of statisitcs for each datafile from a precalculated values
        if(statsDictLoc == ''):
            self.statsDict = {}
        else:
            self.statsDict = self.makeStatsDict(statsDictLoc)

        #This conditional determines whether the glob function will search recursively or not
        if (recur):
            stub = '/**/*'
        else:
            stub = '/*'
        #Makes a list of all files within a specified folder, the files names are their absolute path
        files = [file for file in glob.glob(f'{folder}{stub}')]
        
        #Sub function to help sort files based on year
        def sortByYear(fileName):
            year = fileName[fileName.find('PMID')-5:fileName.find('PMID')-1]
            return int(year)

        if(sort):
            #Sorts files based on year
            sortedFiles = sorted(files,key=sortByYear)
        else:
            sortedFiles = files
        #Chops off all by the first numDatasets datasets
        #print(f'Length of sorted files: {len(sortedFiles)}')
        sortedFiles = sortedFiles[0:numDatasets]

        

        #Initializing dataset list that will hold all datafiles within the passed in folder
        self.datasets = []
        #For each file, add a YeastDataFile to the datasets list
        for f in sortedFiles:
            start = time.time()
            #The data's stats dict is passed to each datafile, and recalc determines whether stats are recalculated or not
            self.datasets.append(YeastDataFile(f,pairs,self.statsDict,subset=subset,recalc=recalc))
            #If dataset mean and standard devation still turn out to be nan, remove it from the datasets list
            if(not isinstance(self.datasets[-1].mean,float) or not isinstance(self.datasets[-1].std,float)):
                del self.datasets[-1]
            #print(f'Time in minutes: {(time.time() - start)/60}')

    #Function that reads in a csv file, then creates a dictionary with file name keys and (mean,std) values
    def makeStatsDict(self,fileName):
        dataTable = pd.read_csv(fileName).to_numpy(dtype=object)
        geneDict = {}
        for row in dataTable:
            geneDict[row[0]] = (row[1],row[2])
        return geneDict
