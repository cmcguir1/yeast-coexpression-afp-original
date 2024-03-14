#!/usr/bin/sh

## Job Created Mar-13-2024

##Place PBS directives here
#PBS -N MultiTerm_L2_PS_Redo_2_0.001_100x50x50
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 2 0.001 100x50x50   > ClusterJobs/MultiTerm_L2_PS_Redo/MultiTerm_L2_PS_Redo30_output.txt