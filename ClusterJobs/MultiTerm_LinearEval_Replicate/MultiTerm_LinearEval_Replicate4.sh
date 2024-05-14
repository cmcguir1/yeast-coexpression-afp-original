#!/usr/bin/sh

## Job Created May-14-2024

##Place PBS directives here
#PBS -N MultiTerm_LinearEval_Replicate_0_200_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 0 200 0   > ClusterJobs/MultiTerm_LinearEval_Replicate/MultiTerm_LinearEval_Replicate4_output.txt