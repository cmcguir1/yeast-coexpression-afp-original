#!/usr/bin/sh

## Job Created Jun-14-2023

##Place PBS directives here
#PBS -N TestClusterSpeed
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py GO:0007005 2000 0.01 0 50 > ClusterJobs/TestClusterSpeed/TestClusterSpeed0_output.txt