import numpy as np

#This class is a con
class ConfusionMatrix:
    def calculateMatrix(data,labelColumn,scoreColumn,accuracy=False,precision=True,recall=True,fpr=True,selectivity=False):
        def calcStats(tp,tn,fp,fn):
            stats = []
            if accuracy:
                stats.append((tp+tn) / (tp+fn+fp+tn))
            if precision:
                stats.append(1 if (tp+fp) == 0 else tp / (tp+fp))
            if recall:
                stats.append(1 if (tp+fn) == 0 else tp / (tp+fn))
            if fpr:
                stats.append(fp / (fp+tn))
            if selectivity:
                stats.append(tn / (tn+fp))
            return np.array(stats)
        
        
        #dataTable = data[data[:,scoreColumn].argsort()[::-1]]
        dataTable = sorted(data,reverse=True,key=lambda row: row[scoreColumn])

        falseNeg = len([row for row in dataTable if row[labelColumn] == 1])
        trueNeg = len([row for row in dataTable if row[labelColumn] == -1])
        falsePos = 0
        truePos = 0

        print(dataTable)
        confusionMatrix = []
        for row in dataTable:
            if row[labelColumn] == 1:
                truePos += 1
                falseNeg -= 1
            elif row[labelColumn] == -1:
                falsePos += 1
                trueNeg -= 1
            confusionMatrix.append(np.concatenate([row,calcStats(tp=truePos,tn=trueNeg,fp=falsePos,fn=falseNeg)],axis=0))

        return confusionMatrix

        
