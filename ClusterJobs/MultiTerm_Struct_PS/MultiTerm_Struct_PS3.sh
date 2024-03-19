#!/usr/bin/sh

## Job Created Mar-19-2024

##Place PBS directives here
#PBS -N MultiTerm_Struct_PS_3_100x50x50
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main9.py 3 100x50x50    > ClusterJobs/MultiTerm_Struct_PS/MultiTerm_Struct_PS3_output.txt