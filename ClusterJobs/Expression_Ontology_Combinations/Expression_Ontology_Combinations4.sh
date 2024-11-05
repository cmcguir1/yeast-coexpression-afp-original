#!/usr/bin/sh

## Job Created Nov-05-2024

##Place PBS directives here
#PBS -N Expression_Ontology_Combinations_0_2022_2007_80x80x80
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py 0 2022 2007 80x80x80  > ClusterJobs/Expression_Ontology_Combinations/Expression_Ontology_Combinations4_output.txt