import pandas as pd
import numpy as np

def compareRankings(ranking,rankingName,other,otherName,cutoff=200,posLoc='./Yeast Resources/positives_00_go04-15-07.txt',negLoc='./Yeast Resources/negatives_00_go04-15-07.txt',agnLoc='./Yeast Resources/agnostic_01_underannotated.txt'):
    posSet = set(list(pd.read_csv(posLoc).to_numpy().flatten()))
    negSet = set(list(pd.read_csv(negLoc).to_numpy().flatten()))
    agnSet = set(list(pd.read_csv(agnLoc).to_numpy().flatten()))

    rankingData = pd.read_csv(ranking).to_numpy()[:,0]
    otherData = pd.read_csv(other).to_numpy()[:,0]
    rankingDict = {}
    for i in range(len(rankingData)):
        rankingDict[rankingData[i]] = i + 1
    otherDict = {}
    for i in range(len(otherData)):
        otherDict[otherData[i]] = i + 1

    dataTable = []
    filteredTable = []
    sharedGenes = list(set(rankingData) & set(otherData))
    for gene in sharedGenes:
        if gene in posSet:
            sign = 1
        elif gene in negSet:
            sign = -1
        else:
            sign = 0
        dataTable.append([gene,sign,rankingDict[gene]+1,otherDict[gene]+1,rankingDict[gene]-otherDict[gene],abs(rankingDict[gene]-otherDict[gene])])
        if(rankingDict[gene] <= cutoff and otherDict[gene] <= cutoff):
            filteredTable.append([gene,sign,rankingDict[gene],otherDict[gene],rankingDict[gene]-otherDict[gene],abs(rankingDict[gene]-otherDict[gene])])
    filteredTable.sort(key=lambda row: row[5],reverse=True)
    dataTable.sort(key=lambda row: row[5],reverse=True)
    pd.DataFrame(dataTable,columns=['Gene','+/0/-',f'{rankingName} rank',f'{otherName} rank',f'Difference ({rankingName}-{otherName})','Absoulte Difference']).to_csv(f'./Yeast Resources/Comparisons/{rankingName}_{otherName}.csv',index=False)
    pd.DataFrame(filteredTable,columns=['Gene','+/0/-',f'{rankingName} rank',f'{otherName} rank',f'Difference ({rankingName}-{otherName})','Absoulte Difference']).to_csv(f'./Yeast Resources/Comparisons/{rankingName}_{otherName}_Filtered_{cutoff}.csv',index=False)

def compareDifference(mefitLoc,pixieLoc,spellLoc,cutoff=100):
    mefit = pd.read_csv(mefitLoc).to_numpy()[:cutoff,0]
    mefitDict = {}
    for i in range(len(mefit)):
        mefitDict[mefitDict[i]] = i + 1

    pixie = pd.read_csv(pixieLoc).to_numpy()[:cutoff,0]
    pixieDict = {}
    for i in range(len(pixie)):
        pixieDict[pixieDict[i]] = i + 1

    spell = pd.read_csv(spellLoc).to_numpy()[:cutoff,0]
    spellDict = {}
    for i in range(len(spell)):
        spellDict[spellDict[i]] = i + 1

    mefitSet = set(mefit)
    pixieSet = set(pixie)
    spellSet = set(spell)

    intersection = mefitSet & pixieSet & spell
    print(intersection)
    print(len(intersection))
    

#compareRankings('./Yeast Resources/GraphResults/430RankedCM_Fixed.csv','430Net','./Yeast Resources/ConfusionMatrixPixie.csv','PIXIE',cutoff=200)
#compareRankings('./Yeast Resources/GraphResults/430RankedCM_Fixed.csv','430Net','./Yeast Resources/ConfusionMatrixMefit.csv','MEFIT',cutoff=200)
#compareRankings('./Yeast Resources/GraphResults/430RankedCM_Fixed.csv','430Net','./Yeast Resources/ConfusionMatrixSpell.csv','SPELL',cutoff=200)
compareDifference('./Yeast Resources/Comparisons/430Net_MEFIT_Filtered_200.csv','./Yeast Resources/Comparisons/430Net_Pixie_Filtered_200.csv',spellLoc='./Yeast Resources/Comparisons/430Net_SPELL_Filtered_200.csv')


