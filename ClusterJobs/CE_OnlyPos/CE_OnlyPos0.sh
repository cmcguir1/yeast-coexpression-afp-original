#!/usr/bin/sh

## Job Created Jun-27-2023

##Place PBS directives here
#PBS -N CE_OnlyPos
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0 0.01    > ClusterJobs/CE_OnlyPos/CE_OnlyPos0_output.txt