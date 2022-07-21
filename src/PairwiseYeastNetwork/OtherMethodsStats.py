import math
import pandas as pd
import numpy as np

def confusionMatrix(dataArray,col):
    positives = set(pd.read_csv('./Yeast Resources/positives_00_go04-15-07.txt').to_numpy().flatten())
    negatives = set(pd.read_csv('./Yeast Resources/negatives_00_go04-15-07.txt').to_numpy().flatten())
    agnostics = set(pd.read_csv('./Yeast Resources/agnostic_01_underannotated.txt').to_numpy().flatten())
    
    #This section calculate how many positives and negatives there are in the dataset so truePos and trueNeg can be initialized
    pos = 0
    neg = 0
    for row in dataArray:
        if(row[0] in positives and not(math.isnan(row[col]))):
            pos += 1
        elif(row[0] in negatives and not(math.isnan(row[col]))):
            neg += 1
    
    #We will start by asserting all genes are false, so falseNeg is the number of positive genes and trueNeg is the number of negative genes
    truePos = 0
    falsePos = 0
    trueNeg = neg
    falseNeg = pos

    dataTable = []
    #Loop over all rows of the dataset
    for row in dataArray:
        if(not math.isnan(row[col])):
            #If the next gene is positive, then increment truePos and decrement falseNeg
            if(row[0] in positives):
                truePos += 1
                falseNeg -= 1
                acc, pre, recall, fpr, select = calcStats(truePos=truePos,falsePos=falsePos,trueNeg=trueNeg,falseNeg=falseNeg)
                dataTable.append([row[0],row[col],1,0,0,truePos,falsePos,trueNeg,falseNeg,acc,pre,recall,fpr,select])
            #If the next gene is negative, then increment falsePos and decrement trueNeg
            elif(row[0] in negatives):
                falsePos += 1
                trueNeg -= 1
                acc, pre, recall, fpr, select = calcStats(truePos=truePos,falsePos=falsePos,trueNeg=trueNeg,falseNeg=falseNeg)
                dataTable.append([row[0],row[col],0,1,0,truePos,falsePos,trueNeg,falseNeg,acc,pre,recall,fpr,select])
            elif(row[0] in agnostics):
                acc, pre, recall, fpr, select = calcStats(truePos=truePos,falsePos=falsePos,trueNeg=trueNeg,falseNeg=falseNeg)
                dataTable.append([row[0],row[col],0,0,1,truePos,falsePos,trueNeg,falseNeg,acc,pre,recall,fpr,select])

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
data = pd.read_csv('./Yeast Resources/ensembleData_membership.csv',index_col=False)

names = data.columns
#Convert dataframe to numpy array
data = data.to_numpy(dtype=object)
pixieData = np.copy(data)
mefitData = np.copy(data)
spellData = np.copy(data)
#Sort the data by the respective confidence of pixie and mefit in descending order
pixie = pixieData[pixieData[:,8].argsort()][::-1]
mefit = mefitData[mefitData[:,10].argsort()][::-1]
#Sort the data by Spell's rank in ascending order as rank 1 is spell's most confident prediction
spell = spellData[spellData[:,12].argsort()]
#Pass sorted data into confusion matrix function, then convert to data frames
#pixieFrame = pd.DataFrame(confusionMatrix(pixie,8),columns=['Gene','Confidence','Positive','Negative','Agnositc','True Positive','False Positive','True Negative','False Negative','Accuracy','Precision','Recall','False Positive Rate','Selectivity'])
mefitFrame = pd.DataFrame(confusionMatrix(mefit,10),columns=['Gene','Confidence','Positive','Negative','Agnositc','True Positive','False Positive','True Negative','False Negative','Accuracy','Precision','Recall','False Positive Rate','Selectivity'])
#spellFrame = pd.DataFrame(confusionMatrix(spell,12),columns=['Gene','Rank','Positive','Negative','Agnositc','True Positive','False Positive','True Negative','False Negative','Accuracy','Precision','Recall','False Positive Rate','Selectivity'])
#Save Data Frame
#pixieFrame.to_csv('./Yeast Resources/ConfusionMatrixPixie.csv',index=False)
mefitFrame.to_csv('./Yeast Resources/ConfusionMatrixMefit.csv',index=False)
#spellFrame.to_csv('./Yeast Resources/ConfusionMatrixSpell.csv',index=False)

