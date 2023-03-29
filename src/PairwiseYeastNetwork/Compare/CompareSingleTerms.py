import pandas as pd
import numpy as np
import glob

def averagePrecision(inputArray):
                precisionArray = np.copy(inputArray)
                for i in range(len(precisionArray)):
                    if precisionArray[i] > precisionArray[i-1]:
                        precisionArray[i-1] = precisionArray[i]
                return np.mean(precisionArray)

termIndices = pd.read_csv('./src/PairwiseYeastNetwork/GOTermIndexDictionary.csv').to_numpy()
termDict = {term[0]: term[1] for term in termIndices}

folder = './Yeast Resources/Pairwise/Spell/AllrSingleTerms/*'
files = [file for file in glob.glob(folder)]

table = []
for term, index in termDict.items():
    sTerm = f'{term[0:2]}{term[3:]}'
    testFiles = [file for file in files if sTerm in file and 'Val' in file and '2000' in file]
    if len(testFiles) > 3:
        averagePrecs = [averagePrecision(pd.read_csv(file).to_numpy()[:,10]) for file in testFiles]
        avgPrec = sum(averagePrecs)/len(averagePrecs)
        averageMeans = [np.mean(pd.read_csv(file).to_numpy()[:,11]) for file in testFiles]
        avgRecall = sum(averageMeans) / len(averageMeans)
        table.append([term,avgRecall,avgPrec])
    else:
        table.append([term,'NA','NA'])

pd.DataFrame(table,columns=['Go-Term','AUC','Avg Prec']).to_csv('./src/PairwiseYeastNetwork/Compare/SingleTermAUC&AvgPrec.csv',index=False)

    
