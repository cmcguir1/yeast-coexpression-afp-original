#!/usr/bin/sh

## Job Created Jan-23-2024

##Place PBS directives here
#PBS -N Parser_AllRoots_1_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 1 0    > ClusterJobs/Parser_AllRoots/Parser_AllRoots1_output.txt