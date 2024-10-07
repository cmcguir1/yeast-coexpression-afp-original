#!/usr/bin/sh

## Job Created Oct-07-2024

##Place PBS directives here
#PBS -N ConsistencyReplicates_SameFold_0_13
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main6.py 0 13    > ClusterJobs/ConsistencyReplicates_SameFold/ConsistencyReplicates_SameFold8_output.txt