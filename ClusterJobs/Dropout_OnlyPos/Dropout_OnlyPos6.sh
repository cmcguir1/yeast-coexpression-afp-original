#!/usr/bin/sh

## Job Created Jul-17-2023

##Place PBS directives here
#PBS -N Dropout_OnlyPos
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 2 0.3    > ClusterJobs/Dropout_OnlyPos/Dropout_OnlyPos6_output.txt