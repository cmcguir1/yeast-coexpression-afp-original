#!/usr/bin/sh

## Job Created Mar-27-2024

##Place PBS directives here
#PBS -N MultiTerm_L2_PS_Redo_0_0.0001_500x200x100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 0 0.0001 500x200x100   > ClusterJobs/MultiTerm_L2_PS_Redo/MultiTerm_L2_PS_Redo1_output.txt