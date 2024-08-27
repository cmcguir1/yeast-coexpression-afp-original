#!/usr/bin/sh

## Job Created Aug-27-2024

##Place PBS directives here
#PBS -N ConsistencyReplicates_DiffFold_0_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0 0    > ClusterJobs/ConsistencyReplicates_DiffFold/ConsistencyReplicates_DiffFold0_output.txt