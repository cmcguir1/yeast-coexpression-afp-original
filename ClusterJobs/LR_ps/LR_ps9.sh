#!/usr/bin/sh

## Job Created Jun-20-2023

##Place PBS directives here
#PBS -N LR_ps
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 1 0.0001    > ClusterJobs/LR_ps/LR_ps9_output.txt