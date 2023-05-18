import pandas as pd
import numpy as np
import sys

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

def compare(filePath):
    ensemble = pd.read_csv('./Yeast Resources/ensembleData.csv').to_numpy()
    singleTerm = pd.read_csv('./Yeast Resources/GraphResults/AllSingle_New/GO0007005_SingleGeneRanking_OnlyPos.csv').to_numpy()
    ranking = pd.read_csv(filePath).to_numpy()

    ensembleGenes = set(ensemble[:,0])
    stGenes = set(singleTerm[:,0])

    mefitSorted = sorted(ensemble,reverse=True,key=lambda row: row[7])
    pixieSorted = sorted(ensemble,reverse=True,key=lambda row: row[5])
    

    mefitMap = {}
    for i in range(len(mefitSorted)):
        mefitMap[mefitSorted[i][0]] = i+1
    
    pixieMap = {}
    for i in range(len(mefitSorted)):
        pixieMap[pixieSorted[i][0]] = i+1

    spellMap = {}
    for row in ensemble:
        spellMap[row[0]] = row[9]

    stMap = {}
    for i in range(len(singleTerm)):
        stMap[singleTerm[i,0]] = i+1

    origPos = set(getGenes('GO:0007005',dataset='original'))
    modernPos = set(getGenes('GO:0007005',dataset='modern'))

    origLeaves = getLeaves(10,dataset='original')
    origNeg = set()
    for leaf in origLeaves:
        if leaf[0] != 'GO:0007005':
            origNeg = origNeg.union(leaf[1])
    origNeg = origNeg - origPos

    modernLeaves = getLeaves(10,dataset='modern')
    modernNeg = set()
    for leaf in modernLeaves:
        if leaf[0] != 'GO:0007005':
            modernNeg = modernNeg.union(leaf[1])
    modernNeg = modernNeg - modernPos
     

    

    compareList = []
    for i in range(len(ranking)):
        gene = ranking[i,0]
        
        if gene in origPos:
            oLabel = 1
        elif gene in origNeg:
            oLabel = -1
        else:
            oLabel = 0

        if gene in modernPos:
            mLabel = 1
        elif gene in modernNeg:
            mLabel = -1
        else:
            mLabel = 0
        
        if gene in ensembleGenes and gene in stGenes:
            compareList.append([gene,oLabel,mLabel,ranking[i,2]/len(origPos),ranking[i,3]/len(ranking),i+1,stMap[gene],spellMap[gene],mefitMap[gene],pixieMap[gene],i+1-stMap[gene],i+1-spellMap[gene],i+1-mefitMap[gene],i+1-pixieMap[gene]])
    rankedGenes = sorted(compareList,reverse=False,key=lambda row: row[5])
    print(rankedGenes)
    pd.DataFrame(rankedGenes,columns=['Gene','Original Label','Modern Label','Confidence','Background Confidence','AG Rank','ST Rank','SPELL Rank','MEFIT Rank','bioPIXIE Rank','ST Diff','SPELL Diff','MEFIT Diff','bioPIXIE Diff']).to_csv('./RankingComparison.csv',index=False)

    # filteredRanking = filter((lambda row: row[3] <= 1000),rankedGenes)
    # pd.DataFrame(filteredRanking,columns=['Gene','Original Label','Modern Label','NN Rank','Spell Rank','Difference']).to_csv('./RankingComparison_Filtered.csv',index=False)
        

compare('./Yeast Resources/GraphResults/MemMap_Original_113x2000x92/GO-0007005_GeneRanking.csv')