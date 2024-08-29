#!/usr/bin/sh

## Job Created Aug-29-2024

##Place PBS directives here
#PBS -N ConsistencyReplicates_DiffFold_0_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0 1    > ClusterJobs/ConsistencyReplicates_DiffFold/ConsistencyReplicates_DiffFold1_output.txt