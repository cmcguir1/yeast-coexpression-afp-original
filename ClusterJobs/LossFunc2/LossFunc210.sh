#!/usr/bin/sh

## Job Created Jun-21-2023

##Place PBS directives here
#PBS -N LossFunc2
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 2 MSE    > ClusterJobs/LossFunc2/LossFunc210_output.txt