#!/usr/bin/sh

## Job Created May-17-2024

##Place PBS directives here
#PBS -N MultiTerm_LinearEval_Replicate_Parallel_0_200_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 0 200 1   > ClusterJobs/MultiTerm_LinearEval_Replicate_Parallel/MultiTerm_LinearEval_Replicate_Parallel1_output.txt