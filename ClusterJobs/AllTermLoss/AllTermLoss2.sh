#!/usr/bin/sh

## Job Created Feb-07-2024

##Place PBS directives here
#PBS -N AllTermLoss_2
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 2     > ClusterJobs/AllTermLoss/AllTermLoss2_output.txt