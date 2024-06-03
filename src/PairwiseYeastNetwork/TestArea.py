from scipy.stats import kstest
from scipy import stats
import random
import pandas as pd

ensemble = pd.read_csv('./Yeast Resources/ensembleData.csv')
nn_table = pd.read_csv('Yeast Resources/GraphResults/MultiTerm_NetStruct_PS/Replicate_0_113x500x200x100x79_GeneRanking_GO0007005.csv')



spell_rank = {}
mefit_rank = {}
pixie_rank = {}
nn_rank = {}
anno = {}
s, m, p, n = 0, 0, 0, 0

for index, row in ensemble.sort_values('Spell Rank',ascending=True).iterrows():
    if not pd.isna(row['Spell Rank']):
        spell_rank[row['ORF']] = s
        s += 1

for index, row in ensemble.sort_values('MEFIT Confidence',ascending=False).iterrows():
    if not pd.isna(row['MEFIT Confidence']):
        mefit_rank[row['ORF']] = m
        m += 1

for index, row in ensemble.sort_values('bioPIXIE Confidence',ascending=False).iterrows():
    if not pd.isna(row['bioPIXIE Confidence']):
        pixie_rank[row['ORF']] = p
        p += 1

for index, row in nn_table.sort_values('Score',ascending=False).iterrows():
    if not pd.isna(row['Score']):
        nn_rank[row['Gene']] = n
        n += 1
    anno[row['Gene']] = row['Annos']

spell_data = [(index/len(spell_rank),anno[gene]) for gene, index in spell_rank.items() if gene in anno]
mefit_data = [(index/len(mefit_rank),anno[gene]) for gene, index in mefit_rank.items() if gene in anno]
pixie_data = [(index/len(pixie_rank),anno[gene]) for gene, index in pixie_rank.items() if gene in anno]
nn_data = [(index/len(nn_rank),anno[gene]) for gene, index in nn_rank.items() if gene in anno]

def divideClasses(data):
    classes = {}
    for label in ['0/0','0/+','0/-','-/0','-/+','-/-','+/0','+/+','+/-']:
        classes[label] = [rank for (rank, a) in data if a == label]
    classes['0/:'] = [rank for rank, a in data if a[0] == '0']
    classes['+/:'] = [rank for rank, a in data if a[0] == '+']
    classes['-/:'] = [rank for rank, a in data if a[0] == '-']
    classes[':/0'] = [rank for rank, a in data if a[2] == '0']
    classes[':/+'] = [rank for rank, a in data if a[2] == '+']
    classes[':/-'] = [rank for rank, a in data if a[2] == '-']
    classes['same'] = [rank for rank, a in data if a[0] == a[2]]
    classes['diff'] = [rank for rank, a in data if a[0] != a[2]]
    return classes

nn_classes = divideClasses(nn_data)
spell_classes = divideClasses(spell_data)
mefit_classes = divideClasses(mefit_data)
pixie_classes = divideClasses(pixie_data)

def ks(classes):
    stats = []
    for label, vector in classes.items():
        stats.append(kstest(vector,'uniform').pvalue)
    return stats

nn_stats = ks(nn_classes)
spell_stats = ks(spell_classes)
mefit_stats = ks(mefit_classes)
pixie_stats = ks(pixie_classes)

columns = ['0/0','0/+','0/-','-/0','-/+','-/-','+/0','+/+','+/-','0/:','+/:','-/:',':/0',':/+',':/-','same','diff']
pd.DataFrame([nn_stats,spell_stats,mefit_stats,pixie_stats],columns=columns).to_csv('./KStest_stats.csv',index=False)

    





