from Ontology import Ontology
import pandas as pd
import numpy as np

def getGenes(goTerm):
    go = Ontology('./obopy/go-basic.obo','./obopy/sgd.gaf',loadLocal=True)
    meiosis1 = go.terms[goTerm]
    genes = meiosis1.allAnnos()
    return getYORF(genes)
    
def makePosNegFiles(goTerm):
    termPositives = getGenes(goTerm)
    leaves = getLeaves(0)
    allGenes = set()
    for leaf in leaves:
        allGenes = allGenes | leaf[1]
    termNegatives = list(allGenes - set(termPositives))
    termAgnostics = set(getGenes('GO:0008150')) - (set(termPositives) | set(termNegatives))
    pd.DataFrame(termPositives).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Pos.txt',index=False,header=False)
    pd.DataFrame(termNegatives).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Neg.txt',index=False,header=False)
    pd.DataFrame(termAgnostics).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Agn.txt',index=False,header=False)

#Searches through a set of genes and returns a list of all of the open reading frame (ORF) names for that set of genes
def getYORF(genes):
    yorfList =[]
    #Loop over all genes in sets
    for gene in genes:
        #Loop over all names for that gene
        for name in gene.aliases:
            #If name matches character requirements, and adds to yorfList
            if(len(name) >= 7 and name[0] == 'Y' and (name[2] == 'L' or name[2] == 'R') and name[3:5].isdigit() and (name[6] == 'W' or name[6] == 'C')):
                yorfList.append(name)
    return yorfList

#Get all GO terms that are leaves
def getLeaves(cutoff):
    #Initialize a gene ontology
    go = Ontology('./obopy/goslim_yeast.obo','./obopy/sgd.gaf',loadLocal=True)
    #Loop over all terms of the ontology
    for term in go.terms:
        #Loop over all parents of a term and add that term to each parent's set of children
        for parent in go.terms[term].parents():
            parent.children.add(term)
    #Loop over all terms, add all terms with no children to list of leaves
    leaves = []
    for term in go.terms:
        if(len(go.terms[term].children) == 0):
            leaves.append(term)
    
    
    leaves = list(filter(lambda leaf: len(getYORF(go.terms[leaf].allAnnos())) >= cutoff,leaves))
    
    leafGenes = []
    for leaf in leaves:
        leafGenes.append((leaf,set(getYORF(go.terms[leaf].allAnnos()))))
    return leafGenes



def getLeafGenes(cutoff):
    leaves = getLeaves()
    print(len(leaves))
    filter(lambda leaf: len(leaf) >= cutoff)
    print(len(leaves))



# mitoGenes = getGenes('GO:0007005')
# print(mitoGenes)
# print(len(mitoGenes))

makePosNegFiles('GO:0007005')






