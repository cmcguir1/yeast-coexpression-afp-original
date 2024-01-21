from Ontology import Ontology
from OntoTerm import OntoTerm
from Gene import Gene

class GOParser():
    def __init__(self,ontoDate,ontoFile='',ontoAnnos='',slimFile=''):
        
        if ontoDate == '2007' or ontoDate == 'original':
            file = './obopy/gene_ontology_2007_Jan.obo'
            annos = './obopy/gene_association.sgd.20070415/gene_association.sgd'
        elif ontoDate == '2009':
            file = 'obopy/gene_ontology_2009_Jan.obo'
            annos = './obopy/sgd_2009_Jan_unzip.gaf'
        else:
            file = './obopy/go-basic.obo'
            annos = './obopy/sgd.gaf'

        if ontoFile != '':
            file = ontoFile
        if ontoAnnos != '':
            annos = ontoAnnos

        self.onto = Ontology(file,annos,loadLocal=True)
        self.assignChildren(self.onto)

        self.numGenes = len(self.onto.genes)


        if slimFile != '':
            sFile = slimFile
        else:
            sFile = './obopy/goslim_yeast.obo'

        self.slim = Ontology(sFile,annos,loadLocal=True)
        self.assignChildren(self.slim)


    def assignChildren(self,ontology):
        for id, term in ontology.terms.items():
            for parent in term.parents():
                parent.children.add(term)

    def getGenes(self,term,direct=False):
        ontoTerm = self.onto.terms[term]
        if direct:
            genes = ontoTerm.directAnnos()
        else:
            genes = ontoTerm.allAnnos()

        yorfList = set()
        #Loop over all genes in sets
        for gene in genes:
            #Loop over all names for that gene
            for name in gene.aliases:
                #If name matches character requirements, and adds to yorfList
                if(len(name) >= 7 and name[0] == 'Y' and (name[2] == 'L' or name[2] == 'R') and name[3:5].isdigit() and (name[6] == 'W' or name[6] == 'C')):
                    yorfList.add(name)
        return yorfList


    def getSlimLeaves(self,cutoff=10,roots='b',childDepth=0,onlyLeaves=True):
        bioProc = self.slim.terms['GO:0008150']
        cellComp = self.slim.terms['GO:0005575']
        molFunc = self.slim.terms['GO:0003674']
        def rootFilter(term):
            ancestors = term.ancestors()
            return (bioProc in ancestors and 'b' in roots) or (cellComp in ancestors and 'c' in roots) or (molFunc in ancestors and 'm' in roots)
        
        
        # availableTerms = set(self.slim.terms.values())
        # for i in range(childDepth):
        #     temp = availableTerms.copy()
        #     for term in availableTerms:
        #         temp = temp.union(term.children)
        #     availableTerms = temp

        leaves = []
        for id, term in self.slim.terms.items():
            if id in self.onto.terms and rootFilter(term):
                
                termGenes = self.getGenes(id)

                
                if len(termGenes) >= cutoff and (len(self.slim.terms[id].children) == 0 or (not onlyLeaves)):
                    leaves.append((id,termGenes))
        return leaves
    
    def smallestCommonAncestor(self,geneA,geneB,leaves):
        A_terms = []
        B_terms = []
        for term, termGenes in leaves:
            if geneA in termGenes:
                A_terms.append(term)
            if geneB in termGenes:
                B_terms.append(term)
        A_ancestors = set.union(*[self.onto.terms[term].ancestors() for term in A_terms])
        B_ancestors = set.union(*[self.onto.terms[term].ancestors() for term in B_terms])
        sharedAncestors = A_ancestors.union(B_ancestors)

        minGenes = 0
        for term in sharedAncestors:
            pass




            


# go = GOParser('2007')
# print(len(go.onto.genes))
# leaves = go.getSlimLeaves(roots='b',childDepth=1)
# allGenes = set()
# for (term, genes) in leaves:
#     allGenes = allGenes.union(genes)
# print(len(leaves))
# print(len(allGenes))
