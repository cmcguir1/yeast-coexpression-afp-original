#!/usr/bin/sh

## Job Created Oct-27-2024

##Place PBS directives here
#PBS -N Expression_Ontology_Combinations_0_2007_2022_20x20x20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py 0 2007 2022 20x20x20  > ClusterJobs/Expression_Ontology_Combinations/Expression_Ontology_Combinations24_output.txt