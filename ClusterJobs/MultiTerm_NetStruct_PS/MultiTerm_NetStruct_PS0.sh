#!/usr/bin/sh

## Job Created May-20-2024

##Place PBS directives here
#PBS -N MultiTerm_NetStruct_PS_0_200_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 0 200 0   > ClusterJobs/MultiTerm_NetStruct_PS/MultiTerm_NetStruct_PS0_output.txt