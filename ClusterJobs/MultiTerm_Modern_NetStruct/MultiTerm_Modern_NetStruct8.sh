#!/usr/bin/sh

## Job Created Jun-10-2024

##Place PBS directives here
#PBS -N MultiTerm_Modern_NetStruct_0_1000x500x200_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 0 1000x500x200 0   > ClusterJobs/MultiTerm_Modern_NetStruct/MultiTerm_Modern_NetStruct8_output.txt