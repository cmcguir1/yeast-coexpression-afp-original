#!/usr/bin/sh

## Job Created Nov-03-2024

##Place PBS directives here
#PBS -N Expression_Ontology_Combinations_1_2022_2007_20x20x20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py 1 2022 2007 20x20x20  > ClusterJobs/Expression_Ontology_Combinations/Expression_Ontology_Combinations21_output.txt