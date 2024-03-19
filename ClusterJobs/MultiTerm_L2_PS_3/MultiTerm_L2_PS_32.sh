#!/usr/bin/sh

## Job Created Mar-19-2024

##Place PBS directives here
#PBS -N MultiTerm_L2_PS_3_2_0.0005_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 2 0.0005 100   > ClusterJobs/MultiTerm_L2_PS_3/MultiTerm_L2_PS_32_output.txt