#!/usr/bin/sh

## Job Created Jun-10-2024

##Place PBS directives here
#PBS -N MultiTerm_Modern_NetStruct_3_1000_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 3 1000 0   > ClusterJobs/MultiTerm_Modern_NetStruct/MultiTerm_Modern_NetStruct7_output.txt