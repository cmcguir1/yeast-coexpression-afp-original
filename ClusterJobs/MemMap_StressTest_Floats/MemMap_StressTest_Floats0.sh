#!/usr/bin/sh

## Job Created May-01-2024

##Place PBS directives here
#PBS -N MemMap_StressTest_Floats_../Cluster_
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/TestMain3.py ../Cluster_     > ClusterJobs/MemMap_StressTest_Floats/MemMap_StressTest_Floats0_output.txt