import pandas as pd
import numpy as np
import glob

def averagePrecision(inputArray):
                precisionArray = np.copy(inputArray)
                for i in range(len(precisionArray)):
                    if precisionArray[i] > precisionArray[i-1]:
                        precisionArray[i-1] = precisionArray[i]
                return np.mean(precisionArray)

termIndices = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary_BioProcOnly.csv').to_numpy()
termDict = {term[0]: term[1] for term in termIndices}

folder = './Yeast Resources/GraphResults/SingleTerms_20/*'
files = [file for file in glob.glob(folder)]

st_rankings = [file for file in files if 'SingleGeneRanking.csv' in file]




table = []
for term, index in termDict.items():
    sTerm = f'{term[0:2]}{term[3:]}'
    if not f'./Yeast Resources/GraphResults/SingleTerms_20\\{sTerm}_SingleGeneRanking.csv' in st_rankings:
        print(sTerm)


    