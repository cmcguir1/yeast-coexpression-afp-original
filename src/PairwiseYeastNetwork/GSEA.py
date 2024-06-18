import pandas as pd
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support
import os

import sys
sys.path.insert(0,'./obopy')
from GOParser import GOParser

parser = GOParser('2023')

common = {}
commonDf = pd.read_csv('./src/PairwiseYeastNetwork/YorfToCommon.csv')
for index, row in commonDf.iterrows():
    common[row['YORF']] = row['Common']

def ES(df,col,term,p=1,commonNames=False):
    genes = parser.getGenes(term)
    running = 0
    maxES = 0
    maxES_index = 0

    df = df.sort_values(by=col,ascending=False)

    corrVector = df[col].to_numpy(dtype=np.float32)
    geneVector = df['Gene'].to_numpy(dtype='U10')
    
    if len(set(df['Gene']) & genes) == 0 or len(geneVector) == len(genes):
        return (None,set(),None)
    else:
        
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
        LES = []
        if maxES > 0:
            for i in range(maxES_index):
                if geneVector[i] in genes:
                    name = (common[geneVector[i]] if geneVector[i] in common and commonNames else geneVector[i]).replace(',','.')
                    LES.append([name,corrVector[i]])
        else:
            for i in range(len(geneVector)-1,maxES_index-1,-1):
                if geneVector[i] in genes:
                    name = (common[geneVector[i]] if geneVector[i] in common and commonNames else geneVector[i]).replace(',','.')
                    LES.append([name,corrVector[i]])
        
        
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

def calcTerm(term,df,scoreCol,p,commonNames=False):
        # print('Term',term)
        es, les, _ = ES(df,scoreCol,term,p=p,commonNames=commonNames)
        if es is not None:

            es_pi = ES_null(df,scoreCol,term,p=p)
            es_pi_pos, es_pi_neg = splitSigns(es_pi)
            pval = pvalue(es,es_pi_pos,es_pi_neg)

            nes, nes_pi_pos, nes_pi_neg = normalizeES(es,es_pi_pos,es_pi_neg)

            return (term,es,pval,nes,les,nes_pi_pos,nes_pi_neg)
        else:
            return None


def GSEA(df,scoreCol,p=1,termCutoff=10,label='',name='GSEA',bpOnly=True,commonNames=False,folder='./Yeast Resources/GSEA_q/',fdr=0.05):
    
    if not os.path.exists(f'{folder}{name}LES/'):
        os.mkdir(f'{folder}{name}LES/')

    bioProc = parser.onto.terms['GO:0008150']
    cellComp = parser.onto.terms['GO:0005575']
    molFunc = parser.onto.terms['GO:0003674']

    def branch(t):
        if t == 'GO:0008150' or bioProc in parser.onto.terms[t].ancestors():
            return 'Biological Process'
        elif t == 'GO:0005575' or cellComp in parser.onto.terms[t].ancestors():
            return 'Cellular Component'
        elif t == 'GO:0003674' or molFunc in parser.onto.terms[t].ancestors():
            return 'Molecular Function'
    
    terms = parser.onto.terms.values()
    bioProcTerms = [term.uid for term in terms if (bioProc in term.ancestors() or not bpOnly) and len(parser.getGenes(term.uid)) > termCutoff] 
    print('Num Terms:',len(bioProcTerms))

    table = []
    pos_nes_terms = []
    neg_nes_terms = []

    nes_pos_dist = []
    nes_neg_dist = []

    nes_pi_pos_dist = []
    nes_pi_neg_dist = []


    executor = ProcessPoolExecutor(max_workers=32)

    threads = []
    for term in bioProcTerms:
        threads.append(executor.submit(calcTerm,term,df,scoreCol,p,commonNames))
    for thread in threads:
        ret = thread.result()
        if ret is not None:
            term,es,pval,nes,les,nes_pi_pos,nes_pi_neg = ret
            if nes > 0:
                nes_pos_dist.append(nes)
                pos_nes_terms.append([term,es,pval,nes,les])
            else:
                nes_neg_dist.append(nes)
                neg_nes_terms.append([term,es,pval,nes,les])
            nes_pi_pos_dist += nes_pi_pos
            nes_pi_neg_dist += nes_pi_neg
        


    pos_nes_terms.sort(key=lambda row: row[3],reverse=False)
    prev_qval = 1000000
    for [term,es,pval,nes,les] in pos_nes_terms:
        NES_star = nes
        pi = len([nes_pi for nes_pi in nes_pi_pos_dist if nes_pi >= NES_star]) / len(nes_pi_pos_dist)
        obs = len([nes_obs for nes_obs in nes_pos_dist if nes_obs >= NES_star]) / len(nes_pos_dist)
        qval = pi / obs
        if qval > prev_qval: qval = prev_qval
        prev_qval = qval
        if qval <= fdr:
            pd.DataFrame(les,columns=['Gene','Correlation']).to_csv(f'{folder}{name}LES/{term.replace(":","-")}_LES.csv',index=False)
        table.append([term,parser.onto.terms[term].name,branch(term),len(parser.getGenes(term)),es,pval,nes,qval,len(les)])
    table.reverse()

    neg_nes_terms.sort(key=lambda row: row[3],reverse=True)
    prev_qval = 1000000
    for [term,es,pval,nes,les] in neg_nes_terms:
        NES_star = nes
        pi = len([nes_pi for nes_pi in nes_pi_neg_dist if nes_pi <= NES_star]) / len(nes_pi_neg_dist)
        obs = len([nes_obs for nes_obs in nes_neg_dist if nes_obs <= NES_star]) / len(nes_neg_dist)
        qval = pi / obs
        if qval > prev_qval: qval = prev_qval
        prev_qval = qval
        if qval <= fdr:
            pd.DataFrame(les,columns=['Gene','Correlation']).to_csv(f'{folder}{name}LES/{term.replace(":","-")}_LES.csv',index=False)
        table.append([term,parser.onto.terms[term].name,branch(term),len(parser.getGenes(term)),es,pval,nes,qval,len(les)])
        


    # nes_pos_dist.sort()
    # NES_star_pos= None
    # for NES_star in nes_pos_dist:

    #     pi = len([nes_pi for nes_pi in nes_pi_pos_dist if nes_pi >= NES_star]) / len(nes_pi_pos_dist)
    #     obs = len([nes_obs for nes_obs in nes_pos_dist if nes_obs >= NES_star]) / len(nes_pos_dist)
    #     fdr_pos = pi / obs
    #     if fdr_pos <= fdr:
    #         NES_star_pos = NES_star
    #         break

    # nes_neg_dist.sort(reverse=True)
    # NES_star_neg= None
    # for NES_star in nes_neg_dist:

    #     pi = len([nes_pi for nes_pi in nes_pi_neg_dist if nes_pi <= NES_star]) / len(nes_pi_neg_dist)
    #     obs = len([nes_obs for nes_obs in nes_neg_dist if nes_obs <= NES_star]) / len(nes_neg_dist)
    #     fdr_neg = pi / obs
    #     if fdr_neg <= fdr:
    #         NES_star_neg = NES_star
    #         break

    pd.DataFrame(table,columns=['GO Term ID','GO Term Name','GO Branch','Num Annotations','ES','p-value',f'NES','FDR q-value','LES size']).to_csv(f'{folder}{name}_{scoreCol.replace(" ","_")}{"_"+label[0]+ "_" + label[2] if label != "" else ""}.csv',index=False)
    print('Done')

if __name__ == '__main__':
    freeze_support()
    
    for label in ['+/+','+/-','-/+','-/-','0/+','0/-','+/0','+/-','0/0']:
        inputData = pd.read_csv('./AnnoRankData.csv')
        inputData['NN'] = inputData['NN'] - 0.5
        inputData['MEFIT'] = inputData['MEFIT'] - 0.5
        inputData['SPELL'] = inputData['SPELL'] - 0.5
        inputData['bioPIXIE'] = inputData['bioPIXIE'] - 0.5

        inputData = inputData.dropna(subset=[sys.argv[1]])
        inputData = inputData[inputData['Anno'] == label]
        

        GSEA(inputData,sys.argv[1],termCutoff=5,label=label,folder='GSEA_redo')

    inputData = pd.read_csv('./AnnoRankData.csv')
    inputData['NN'] = inputData['NN'] - 0.5
    inputData['MEFIT'] = inputData['MEFIT'] - 0.5
    inputData['SPELL'] = inputData['SPELL'] - 0.5
    inputData['bioPIXIE'] = inputData['bioPIXIE'] - 0.5

    inputData = inputData.dropna(subset=[sys.argv[1]])

    


    start = time.time()
    GSEA(inputData,sys.argv[1],termCutoff=5,name='GSEA_redo')
    print('Time:',(time.time()-start)/60,'minutes')





