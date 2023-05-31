import pandas as pd
import numpy as np
import sys

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes

def compare(filePath):
    ensemble = pd.read_csv('./Yeast Resources/ensembleData.csv').to_numpy()
    singleTerm = pd.read_csv('./Yeast Resources/GraphResults/AllSingle_New/GO0007005_SingleGeneRanking_OnlyPos.csv').to_numpy()
    # Ranking where all cell comp and mol func GO terms are included in the output
    allOutput = pd.read_csv('./Yeast Resources/GraphResults/MemMap_Original_113x2000x92/GO-0007005_GeneRanking.csv').to_numpy()
    agLoc = pd.read_csv('./Yeast Resources/GraphResults/BioProc+LocalizationData/136x25000x53_GeneRanking_GO0007005.csv').to_numpy()
    bpData = pd.read_csv('./Yeast Resources/GraphResults/bioPIXIE_Data/149x25000x53_GeneRanking_GO0007005.csv').to_numpy()
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
    
    allOutMap = {}
    for i in range(len(allOutput)):
        allOutMap[allOutput[i,0]] = i+1

    agLocMap = {}
    for i in range(len(agLoc)):
        agLocMap[agLoc[i,0]] = i+1

    bpMap = {}
    for i in range(len(bpData)):
        bpMap[bpData[i,0]] = i+1

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

    mitoLoc = set(getGenes('GO:0005739',dataset='modern'))
     

    

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
            compareList.append([gene,oLabel,mLabel,1 if gene in mitoLoc else -1,ranking[i,2]/len(origPos),ranking[i,3]/len(ranking),i+1,allOutMap[gene],agLocMap[gene],bpMap[gene],stMap[gene],spellMap[gene],mefitMap[gene],pixieMap[gene]])
    rankedGenes = sorted(compareList,reverse=False,key=lambda row: row[6])
    print(rankedGenes)
    pd.DataFrame(rankedGenes,columns=['Gene','Original Label','Modern Label','Mito Localized','Confidence','Background Confidence','AG bioProcOnly Rank','AG AllTerm Rank','AG Local','AG bioPIXIE','ST Rank','SPELL Rank','MEFIT Rank','bioPIXIE Rank']).to_csv('./RankingComparison_Final.csv',index=False)


    # filteredRanking = filter((lambda row: row[3] <= 1000),rankedGenes)
    # pd.DataFrame(filteredRanking,columns=['Gene','Original Label','Modern Label','NN Rank','Spell Rank','Difference']).to_csv('./RankingComparison_Filtered.csv',index=False)
        

compare('./Yeast Resources/GraphResults/BioProcOnly/113x25000x53_GeneRanking_GO0007005.csv')