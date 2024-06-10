from scipy.stats import kstest, ks_2samp
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

for index, row in ensemble.sort_values('Spell Rank',ascending=False).iterrows():
    if not pd.isna(row['Spell Rank']):
        spell_rank[row['ORF']] = s
        s += 1

for index, row in ensemble.sort_values('MEFIT Confidence',ascending=True).iterrows():
    if not pd.isna(row['MEFIT Confidence']):
        mefit_rank[row['ORF']] = m
        m += 1

for index, row in ensemble.sort_values('bioPIXIE Confidence',ascending=True).iterrows():
    if not pd.isna(row['bioPIXIE Confidence']):
        pixie_rank[row['ORF']] = p
        p += 1

for index, row in nn_table.sort_values('Score',ascending=True).iterrows():
    if not pd.isna(row['Score']):
        nn_rank[row['Gene']] = n
        n += 1
    anno[row['Gene']] = row['Annos']

spell_data = [(index/len(spell_rank),anno[gene]) for gene, index in spell_rank.items() if gene in anno]
mefit_data = [(index/len(mefit_rank),anno[gene]) for gene, index in mefit_rank.items() if gene in anno]
pixie_data = [(index/len(pixie_rank),anno[gene]) for gene, index in pixie_rank.items() if gene in anno]
nn_data = [(index/len(nn_rank),anno[gene]) for gene, index in nn_rank.items() if gene in anno]

combined = []
for gene, label in anno.items():
    if gene in spell_rank:
        spell_d = spell_rank[gene] / len(spell_rank)
    else:
        spell_d = None
    if gene in mefit_rank:
        mefit_d = mefit_rank[gene] / len(mefit_rank)
    else:
        mefit_d = None
    if gene in pixie_rank:
        pixie_d = pixie_rank[gene] / len(pixie_rank)
    else:
        pixie_d = None
    if gene in nn_rank:
        nn_d = nn_rank[gene] / len(nn_rank)
    else:
        nn_d = None

    combined.append([gene,label,nn_d,spell_d,mefit_d,pixie_d])
# pd.DataFrame(combined,columns=['Gene','Anno','NN','SPELL','MEFIT','bioPIXIE']).to_csv('./AnnoRankData.csv',index=False)

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



classes = ['0/0','0/+','0/-','-/0','-/+','-/-','+/0','+/+','+/-','0/:','+/:','-/:',':/0',':/+',':/-','same','diff']
model_classes = {'NN':nn_classes,'SPELL':spell_classes,'MEFIT':mefit_classes,'bioPIXIE':pixie_classes}
models = ['NN','SPELL','MEFIT','bioPIXIE']


def compareDist(label,samp1,samp2,alternative):
    data1 = samp1[label]
    data2 = samp2[label]
    return ks_2samp(data1,data2,alternative=alternative).pvalue

# for alt in ['greater','less','two-sided']:
#     table = []
#     for i in range(len(models)):
#         for j in range(i+1,len(models)):
#             samp1 = model_classes[models[i]]
#             samp2 = model_classes[models[j]]
#             row = [f'{models[i]}_{models[j]}'] + [compareDist(label,samp1,samp2,alt) for label in classes]
#             table.append(row)
#     pd.DataFrame(table,columns=['Comparison']+classes).to_csv(f'KS_tests_{alt}.csv',index=False)

def ks(model_classes,alternative):
    stats = []
    for label in classes:
        stats.append(kstest(model_classes[label],'uniform',alternative=alternative).pvalue)
    return stats

for alt in ['greater','less','two-sided']:
    nn_stats = ks(nn_classes,alt)
    spell_stats = ks(spell_classes,alt)
    mefit_stats = ks(mefit_classes,alt)
    pixie_stats = ks(pixie_classes,alt)
    pd.DataFrame([nn_stats,spell_stats,mefit_stats,pixie_stats],columns=classes).to_csv(f'./KStest_randomUniform_{alt}.csv',index=True)




    





