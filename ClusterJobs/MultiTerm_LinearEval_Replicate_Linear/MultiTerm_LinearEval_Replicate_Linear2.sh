#!/usr/bin/sh

## Job Created May-16-2024

##Place PBS directives here
#PBS -N MultiTerm_LinearEval_Replicate_Linear_2_20_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 2 20 0   > ClusterJobs/MultiTerm_LinearEval_Replicate_Linear/MultiTerm_LinearEval_Replicate_Linear2_output.txt