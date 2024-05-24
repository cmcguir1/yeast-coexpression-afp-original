#!/usr/bin/sh

## Job Created May-24-2024

##Place PBS directives here
#PBS -N MultiTerm_NetStruct_Replicates_3_500x200x100_2
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 3 500x200x100 2   > ClusterJobs/MultiTerm_NetStruct_Replicates/MultiTerm_NetStruct_Replicates7_output.txt