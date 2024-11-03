#!/usr/bin/sh

## Job Created Nov-03-2024

##Place PBS directives here
#PBS -N Expression_Ontology_Combinations_1_2007_2022_80x80x80
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py 1 2007 2022 80x80x80  > ClusterJobs/Expression_Ontology_Combinations/Expression_Ontology_Combinations9_output.txt