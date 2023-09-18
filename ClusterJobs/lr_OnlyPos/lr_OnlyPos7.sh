#!/usr/bin/sh

## Job Created Jul-18-2023

##Place PBS directives here
#PBS -N lr_OnlyPos
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3 0.01    > ClusterJobs/lr_OnlyPos/lr_OnlyPos7_output.txt