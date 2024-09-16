#!/usr/bin/sh

## Job Created Sep-16-2024

##Place PBS directives here
#PBS -N ConsistencyReplicates_DiffFold_0_19
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0 19    > ClusterJobs/ConsistencyReplicates_DiffFold/ConsistencyReplicates_DiffFold14_output.txt