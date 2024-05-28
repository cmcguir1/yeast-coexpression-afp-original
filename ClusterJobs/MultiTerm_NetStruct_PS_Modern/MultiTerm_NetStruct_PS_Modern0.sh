#!/usr/bin/sh

## Job Created May-28-2024

##Place PBS directives here
#PBS -N MultiTerm_NetStruct_PS_Modern_0_500x200x100_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 0 500x200x100 0   > ClusterJobs/MultiTerm_NetStruct_PS_Modern/MultiTerm_NetStruct_PS_Modern0_output.txt