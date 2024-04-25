#!/usr/bin/sh

## Job Created Apr-25-2024

##Place PBS directives here
#PBS -N MemMap_Debug_0_0_500x200x100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 0 0 500x200x100   > ClusterJobs/MemMap_Debug/MemMap_Debug0_output.txt