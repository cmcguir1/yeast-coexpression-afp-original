import pandas as pd
import numpy as np
import time

import sys
sys.path.insert(0,'./obopy')
from GOParser import GOParser

parser = GOParser('2023')

def ES(df,col,term,p=1):
    genes = parser.getGenes(term)
    running = 0
    maxES = 0
    maxES_index = 0

    df = df.sort_values(by=col,ascending=False)

    corrVector = df[col].to_numpy(dtype=np.float32)
    geneVector = df['Gene'].to_numpy(dtype='U10')
    
    table = []
    
    # Calculate N_r value
    N_r = 0
    for i in range(len(corrVector)):
        if geneVector[i] in genes:
            N_r += pow(abs(corrVector[i]),p)
    
    

    # Calculate running score and ES value
    for i in range(len(corrVector)):
        if geneVector[i] in genes:
            running += pow(abs(corrVector[i]),p) / N_r
        else:
            running -= 1 / (len(corrVector) - len(genes))

        # table.append([i,running,geneVector[i],1 if geneVector[i] in genes else 0])

        if abs(running) > abs(maxES):
            maxES = running
            maxES_index = i

    # Generate leading-edge subset based on maxES
    LES = set()
    if maxES > 0:
        for i in range(maxES_index):
            if geneVector[i] in genes:
                LES.add(geneVector[i])
    else:
        for i in range(len(geneVector)-1,maxES_index-1,-1):
            if geneVector[i] in genes:
                LES.add(geneVector[i])
    
    
    return (maxES,LES,table)

def ES_null(df,col,term,p=1):
    df = df.copy()
    dist = []
    for i in range(1000):
        df[col] = np.random.permutation(df[col])
        es, les, _ = ES(df,col,term,p=p)
        dist.append(es)
    return dist

def splitSigns(arr):
    pos = []
    neg = []
    for x in arr:
        if x > 0: pos.append(x)
        else: neg.append(x)
    return (pos,neg)

def pvalue(es,pos,neg):
    pos.sort(reverse=False)
    neg.sort(reverse=True)
    if es > 0:
        for i in range(len(pos)):
            if es < pos[i]:
                return (len(pos) - i) / len(pos)
        return 0
    else:
        for i in range(len(neg)):
            if es > neg[i]:
                return (len(neg) - i) / len(neg)
        return 0
    
def normalizeES(es,es_pi_pos,es_pi_neg):
    mean_pos = abs(sum(es_pi_pos) / len(es_pi_pos)) if len(es_pi_pos) != 0 else 1
    mean_neg = abs(sum(es_pi_neg) / len(es_pi_neg)) if len(es_pi_neg) != 0 else 1

    if es > 0: nes = es / mean_pos
    else: nes = es/ mean_neg

    nes_pi_pos = [x / mean_pos for x in es_pi_pos]
    nes_pi_neg = [x / mean_neg for x in es_pi_neg]
    
    return (nes,nes_pi_pos,nes_pi_neg)




def GSEA(df,scoreCol,fdr,p=1,termCutoff=10):
    
    bioProc = parser.onto.terms['GO:0008150']
    terms = parser.onto.terms.values()
    bioProcTerms = [term.uid for term in terms if bioProc in term.ancestors() and len(parser.getGenes(term.uid)) > termCutoff]
    print('Num Terms:',len(bioProcTerms))

    table = []

    nes_pos_dist = []
    nes_neg_dist = []

    nes_pi_pos_dist = []
    nes_pi_neg_dist = []

    for term in bioProcTerms:
        es, les, _ = ES(df,scoreCol,term,p=p)
        les_str = ';'.join(les)
        es_pi = ES_null(df,scoreCol,term,p=p)
        es_pi_pos, es_pi_neg = splitSigns(es_pi)
        pval = pvalue(es,es_pi_pos,es_pi_neg)

        nes, nes_pi_pos, nes_pi_neg = normalizeES(es,es_pi_pos,es_pi_neg)

        if nes > 0: nes_pos_dist.append(nes)
        else: nes_neg_dist.append(nes)

        nes_pi_pos_dist += nes_pi_pos
        nes_pi_neg_dist += nes_pi_neg

        table.append([term,parser.onto.terms[term].name,es,pval,nes,les_str])
    
    nes_pos_dist.sort()
    NES_star_pos= None
    for NES_star in nes_pos_dist:

        pi = len([nes_pi for nes_pi in nes_pi_pos_dist if nes_pi >= NES_star]) / len(nes_pi_pos_dist)
        obs = len([nes_obs for nes_obs in nes_pos_dist if nes_obs >= NES_star]) / len(nes_pos_dist)
        fdr_pos = pi / obs
        if fdr_pos <= fdr:
            NES_star_pos = NES_star
            break

    nes_neg_dist.sort(reverse=True)
    NES_star_neg= None
    for NES_star in nes_neg_dist:

        pi = len([nes_pi for nes_pi in nes_pi_neg_dist if nes_pi <= NES_star]) / len(nes_pi_neg_dist)
        obs = len([nes_obs for nes_obs in nes_neg_dist if nes_obs <= NES_star]) / len(nes_neg_dist)
        fdr_neg = pi / obs
        if fdr_neg <= fdr:
            NES_star_neg = NES_star
            break

    pd.DataFrame(table,columns=['GO Term ID','GO Term Name','ES','p-value',f'NES (NES*_pos = {NES_star_pos};NES*_neg={NES_star_neg}))','Leading-edge subset']).to_csv(f'./Yeast Resources/GSEA/GSEA_{scoreCol}.csv',index=False)
    


inputData = pd.read_csv('./AnnoRankData.csv')
inputData['NN'] = inputData['NN'] - 0.5
inputData['MEFIT'] = inputData['MEFIT'] - 0.5
inputData['SPELL'] = inputData['SPELL'] - 0.5
inputData['bioPIXIE'] = inputData['bioPIXIE'] - 0.5

inputData = inputData.dropna(subset=[sys.argv[1]])

GSEA(inputData,sys.argv[1],0.05,termCutoff=10)





