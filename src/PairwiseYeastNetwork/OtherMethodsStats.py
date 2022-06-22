import math
import pandas as pd
import numpy as np
from sqlalchemy import false

def confusionMatrix(dataArray,col):
    #This section calculate how many positives and negatives there are in the dataset so truePos and trueNeg can be initialized
    pos = 0
    neg = 0
    for row in dataArray:
        if(row[4] == 1):
            pos += 1
        elif(row[2] == 0):
            neg += 1
    
    #We will start by asserting all genes are true, so truePos is the number of positive genes and trueNeg is the number of negative genes
    truePos = pos
    falsePos = neg
    trueNeg = 0
    falseNeg = 0

    dataTable = []
    #Loop over all rows of the dataset
    for row in dataArray:
        if(not math.isnan(row[col])):
            #If the next gene is positive, then increment false negative and decrement true positive
            if(row[4] == 1):
                truePos -= 1
                falseNeg += 1
                acc, pre, recall, fpr, select = calcStats(truePos=truePos,falsePos=falsePos,trueNeg=trueNeg,falseNeg=falseNeg)
                dataTable.append([row[0],row[col],truePos,falsePos,trueNeg,falseNeg,acc,pre,recall,fpr,select])
            #If the next gene is negative, then increment true negative, and decrement false positive
            elif(row[2] == 0):
                falsePos -= 1
                trueNeg += 1
                acc, pre, recall, fpr, select = calcStats(truePos=truePos,falsePos=falsePos,trueNeg=trueNeg,falseNeg=falseNeg)
                dataTable.append([row[0],row[col],truePos,falsePos,trueNeg,falseNeg,acc,pre,recall,fpr,select])
    #Return dataTable as an array
    return np.array(dataTable)

#Calculate confusion matrix statistics for a confusion matrix
def calcStats(truePos,falsePos,trueNeg,falseNeg):
    accuracy = (truePos + trueNeg)/(truePos + trueNeg + falsePos + falseNeg)
    precision = 1 if (truePos + falsePos == 0) else truePos/(truePos+falsePos)
    recall = truePos / (truePos+falseNeg)
    fpr = falsePos / (falsePos + trueNeg)
    selectivity = trueNeg / (trueNeg + falsePos)
    return (accuracy,precision,recall,fpr,selectivity)

#Read in a ensemble data file with no index
data = pd.read_csv('./Yeast Resources/ensembleData.csv',index_col=False)
names = data.columns
#Convert dataframe to numpy array
data = data.to_numpy()
#Sort the data by the respective confidence of pixie and mefit in descending order
pixie = data[data[:,5].argsort()][::-1]
mefit = data[data[:,7].argsort()][::-1]
#Sort the data by Spell's rank in ascending order as rank 1 is spell's most confident prediction
spell = data[data[:,9].argsort()]
#Pass sorted data into confusion matrix function, then convert to data frames
pixieFrame = pd.DataFrame(confusionMatrix(pixie,5),columns=['Gene','Confidence','True Positive','False Positive','True Negative','False Negative','Accuracy','Precision','Recall','False Positive Rate','Selectivity'])
mefitFrame = pd.DataFrame(confusionMatrix(mefit,7),columns=['Gene','Confidence','True Positive','False Positive','True Negative','False Negative','Accuracy','Precision','Recall','False Positive Rate','Selectivity'])
spellFrame = pd.DataFrame(confusionMatrix(spell,9),columns=['Gene','Rank','True Positive','False Positive','True Negative','False Negative','Accuracy','Precision','Recall','False Positive Rate','Selectivity'])
#Save Data Frame
pixieFrame.to_csv('./Yeast Resources/ConfusionMatrixPixie.csv',index=False)
mefitFrame.to_csv('./Yeast Resources/ConfusionMatrixMefit.csv',index=False)
spellFrame.to_csv('./Yeast Resources/ConfusionMatrixSpell.csv',index=False)

