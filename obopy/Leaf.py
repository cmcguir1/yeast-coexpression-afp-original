from Ontology import Ontology
import pandas as pd
import numpy as np

def getGenes(goTerm,dataset = 'modern',direct=False):
    if dataset == '2007' or dataset == 'original':
        go = Ontology('./obopy/gene_ontology_2007_Jan.obo','./obopy/gene_association.sgd.20070415/gene_association.sgd',loadLocal=True)
    else:
        go = Ontology('./obopy/go-basic.obo','./obopy/sgd.gaf',loadLocal=True)
    term = go.terms[goTerm]
    if direct:
        genes = term.directAnnos()
    else:
        genes = term.allAnnos()
    return getYORF(genes)

def printName(goTerm,dataset = 'modern'):
    if dataset == '2007' or dataset == 'original':
        go = Ontology('./obopy/gene_ontology_2007_Jan.obo','./obopy/gene_association.sgd.20070415/gene_association.sgd',loadLocal=True)
    else:
        go = Ontology('./obopy/go-basic.obo','./obopy/sgd.gaf',loadLocal=True)
    term = go.terms[goTerm]
    print(term.name)
    
def makePosNegFiles(goTerm,dataset='original'):
    termPositives = getGenes(goTerm,dataset=dataset)
    leaves = getLeaves(10,dataset='original',exclude=['GO:0002181','GO:0022857','GO:0032543'])
    allGenes = set()
    for leaf in leaves:
        allGenes = allGenes | leaf[1]
    termNegatives = list(allGenes - set(termPositives))
    termAgnostics = set(getGenes('GO:0008150')) - (set(termPositives) | set(termNegatives))
    pd.DataFrame(termPositives).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Pos_{dataset}.txt',index=False,header=False)
    pd.DataFrame(termNegatives).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Neg_{dataset}.txt',index=False,header=False)
    pd.DataFrame(termAgnostics).to_csv(f'./Yeast Resources/GeneSets/{goTerm[0:2] + goTerm[3:]}_Agn_{dataset}.txt',index=False,header=False)

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

#Get all GO terms that are leaves, each leaf being a tuple of the leaf term name and a set of all genes annotated to that term
def getLeaves(cutoff,dataset='original',bioProc=True,molFunc=False,cellComp=False,exclude=[]):
    #Initialize the datsets that annotations will be pulled from, either the 2007 dataset or the current 2023 dataset
    if dataset == '2007' or dataset == 'original':
        goAnnos = Ontology('./obopy/gene_ontology_2007_Jan.obo','./obopy/gene_association.sgd.20070415/gene_association.sgd',loadLocal=True)
        
    else:
        goAnnos = Ontology('./obopy/go-basic.obo','./obopy/sgd.gaf',loadLocal=True)
        
    
    #Initialize the go slim ontology that terms will be pulled from
    goSlim = Ontology('./obopy/goslim_yeast.obo','./obopy/sgd.gaf',loadLocal=True)
    #Loop over all terms of the go slim
    for term in goSlim.terms:
        #Loop over all parents of a term and add that term to each parent's set of children
        for parent in goSlim.terms[term].parents():
            parent.children.add(term)

    for term in goAnnos.terms:
        for parent in goAnnos.terms[term].parents():
            parent.children.add(term)
    #print(goSlim.terms)
    def isParent(term,parent):
        
        if parent in term.is_a:
            return True
        elif len(term.is_a) == 0:
            return False
        else:
            return True in [isParent(t,parent) for t in term.is_a]            
                
    def typeFilter(term,slim):
        return ((isParent(term,slim.terms['GO:0008150']) and bioProc) or 
                (isParent(term,slim.terms['GO:0003674']) and molFunc) or 
                (isParent(term,slim.terms['GO:0005575']) and cellComp))

    

    #Loop over all terms, add all terms with no children to list of leaves
    
    
    leaves = []
    for term in goSlim.terms:
        if (not term in exclude) and (len(goSlim.terms[term].children) == 0):
            leaves.append(term)
        # if term in goAnnos.terms and (len(goAnnos.terms[term].children) == 0):
        #     leaves.append(term)
        
    
    leaves = list(filter(lambda leaf: len(getYORF(goSlim.terms[leaf].allAnnos())) >= cutoff,leaves))
    

    leaves = list(filter(lambda term: typeFilter(goAnnos.terms[term],goAnnos),leaves))
    
    leafGenes = []
    for leaf in leaves:
        leafGenes.append((leaf,set(getYORF(goAnnos.terms[leaf].allAnnos()))))
        
        #leafGenes.append((leaf,getGenes(leaf)))
    return leafGenes



def getLeafGenes(cutoff):
    leaves = getLeaves()
    print(len(leaves))
    filter(lambda leaf: len(leaf) >= cutoff)
    print(len(leaves))







