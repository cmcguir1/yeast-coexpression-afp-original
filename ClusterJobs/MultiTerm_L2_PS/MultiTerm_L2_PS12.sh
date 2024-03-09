#!/usr/bin/sh

## Job Created Mar-08-2024

##Place PBS directives here
#PBS -N MultiTerm_L2_PS_0_0.01_500
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 0 0.01 500   > ClusterJobs/MultiTerm_L2_PS/MultiTerm_L2_PS12_output.txt