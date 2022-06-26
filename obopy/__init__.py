
from Ontology import Ontology
import pandas as pd
import numpy as np

def getGenes(goTerm):
    go = Ontology('./obopy/go-basic.obo','./obopy/sgd.gaf',loadLocal=True)
    meiosis1 = go.terms[goTerm]
    genes = meiosis1.allAnnos()
    print(f"Type: {type(genes)}")
    yorfList =[]
    for gene in genes:
        for name in gene.aliases:
            if(len(name) >= 7 and name[0] == 'Y' and (name[2] == 'L' or name[2] == 'R') and name[3:5].isdigit() and (name[6] == 'W' or name[6] == 'C')):
                yorfList.append(name)
    return yorfList

def makePosNegFiles(goTerm):
    termPositives = getGenes('GO:0006302')
    mitoInherPositives = set(pd.read_csv('./Yeast Resources/positives_00_go04-15-07.txt').to_numpy().flatten().tolist())
    mitoInherNegatives = set(pd.read_csv('./Yeast Resources/negatives_00_go04-15-07.txt').to_numpy().flatten().tolist())
    possiblePos = mitoInherPositives | mitoInherNegatives
    termNegatives = list(possiblePos - set(termPositives))
    pd.DataFrame(termPositives).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Pos.txt',index=False,header=False)
    pd.DataFrame(termNegatives).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Neg.txt',index=False,header=False)




makePosNegFiles('GO:0007127')



