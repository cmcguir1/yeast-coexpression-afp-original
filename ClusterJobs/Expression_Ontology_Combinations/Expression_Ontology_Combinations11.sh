#!/usr/bin/sh

## Job Created Nov-23-2024

##Place PBS directives here
#PBS -N Expression_Ontology_Combinations_3_2007_2022_500x200x100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py 3 2007 2022 500x200x100  > ClusterJobs/Expression_Ontology_Combinations/Expression_Ontology_Combinations11_output.txt