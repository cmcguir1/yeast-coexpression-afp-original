#!/usr/bin/sh

## Job Created Apr-23-2024

##Place PBS directives here
#PBS -N MemMap_Debug_1_1e-06_500x200x100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 1 1e-06 500x200x100   > ClusterJobs/MemMap_Debug/MemMap_Debug13_output.txt