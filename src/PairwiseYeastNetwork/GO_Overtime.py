import pandas as pd
import numpy as np
import os, sys
import time

sys.path.insert(0,'./obopy')
from Leaf import getLeaves, getGenes
from GOParser import GOParser

start = time.time()
dates = open('./Yeast Resources/GO_Data/dates_firstOfYear.txt','r')

termNamesData = pd.read_csv('./src/PairwiseYeastNetwork/TermNameDict.csv').to_numpy()
termName = {}
for row in termNamesData:
    termName[row[0]] = row[1]
    
ogParser = GOParser('2007')
modernParser = GOParser('2023')
slim = modernParser.getSlimLeaves()
negGenes = set()
for term, geneSet in slim:
    negGenes = negGenes.union(geneSet)

parsers = []

genes = pd.read_csv('./src/PairwiseYeastNetwork/AllYorfs.csv').to_numpy().flatten()
ogMitoNeg = negGenes - ogParser.getGenes('GO:0007005')
modernMito = modernParser.getGenes('GO:0007005')
neg_pos = ogMitoNeg & modernMito
print(len(neg_pos))

table = []
for gene in ogParser.getGenes('GO:0007005'):
    ogAnnos = []
    modernAnnos = []
    for (term, _) in slim:
        ogGenes = ogParser.getGenes(term)
        if gene in ogGenes:
            ogAnnos.append(f'{term} ({termName[term]})')
        modernGenes = modernParser.getGenes(term)
        if gene in modernGenes:
            modernAnnos.append(f'{term} ({termName[term]})')
    lostAnnos = set(ogAnnos) - set(modernAnnos)
    wrongFunc = 1 if len(set(ogAnnos) - lostAnnos) == 0 else 0
    newFunc = 1 if len(set(ogAnnos) - lostAnnos) > 0 and len(lostAnnos) > 0 else 0
    sameFunc = 1 if wrongFunc == 0 and newFunc == 0 else 0
    table.append([gene,';'.join(ogAnnos),';'.join(modernAnnos),';'.join(lostAnnos),wrongFunc,newFunc,sameFunc])

pd.DataFrame(table,columns=['Gene','Original Annotations','Modern Annotations','Removed Annotations','Wrong Function?','New Function?','Same Function?']).to_csv('./Yeast Resources/GO_Data/Stats/OGMito_Annotations.csv',index=False)
        




# for line in dates.readlines():
#     date = line[:-1]

#     ontoFile = f'./Yeast Resources/GO_Data/{date}/gene_ontology.obo'
#     basicFile = f'./Yeast Resources/GO_Data/{date}/go-basic.obo'   
#     sgdFile = f'./Yeast Resources/GO_Data/{date}/sgd.gaf' 

#     if os.path.exists(basicFile):
#         onto = basicFile
#     elif os.path.exists(ontoFile):
#         onto = ontoFile
#     else:
#         print('No ontology file for',date)
    
#     if os.path.exists(sgdFile):
#         annos = sgdFile
#     else:
#         print('No annotations file for',date)
    
#     parser = GOParser(date,ontoFile=onto,ontoAnnos=annos)
#     parsers.append((date,parser))

# parsers.reverse()
# print('Created Parsers:',(time.time()-start)/60,'minutes')



# annosOvertime = []
# maxNumAnnos = 0
# for date, par in parsers:
#     print(date,(time.time()-start)/60,'minutes')
#     annoNum = {}
#     for gene in genes:
#         annos = 0
#         for (term, _) in slim:
#             if term in par.onto.terms:
#                 termGenes = par.getGenes(term)
#                 if gene in termGenes:
#                     annos += 1
#         if annos in annoNum: annoNum[annos] += 1
#         else: annoNum[annos] = 1
#         maxNumAnnos = max(maxNumAnnos,annos)
#     annosOvertime.append((date,annoNum))

# print('Making Table')
# table = []
# for (date,annoNum) in annosOvertime:
#     dateLst = []
#     for i in range(maxNumAnnos+1):
#         if i in annoNum: dateLst.append(annoNum[i])
#         else: dateLst.append(0)
#     table.append([date]+dateLst)

# pd.DataFrame(table,columns=['Onto Date']+[f'{i}' for i in range(maxNumAnnos+1)]).to_csv('./Yeast Resources/GO_Data/Stats/GeneSlimAnnosOverTime_Modern.csv',index=False)









    

    
    


    