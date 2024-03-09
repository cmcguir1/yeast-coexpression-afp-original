#!/usr/bin/sh

## Job Created Mar-08-2024

##Place PBS directives here
#PBS -N SingleTerm_2.28_3
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main6.py 3     > ClusterJobs/SingleTerm_2.28/SingleTerm_2.283_output.txt