from Ontology import Ontology
from OntoTerm import OntoTerm
from Gene import Gene

goAnnos = Ontology('./obopy/gene_ontology_2007_Jan.obo','./obopy/gene_association.sgd.20070415/gene_association.sgd',loadLocal=True)