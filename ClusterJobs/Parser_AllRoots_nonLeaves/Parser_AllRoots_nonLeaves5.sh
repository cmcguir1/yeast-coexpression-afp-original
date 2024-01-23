#!/usr/bin/sh

## Job Created Jan-23-2024

##Place PBS directives here
#PBS -N Parser_AllRoots_nonLeaves_1_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 1 1    > ClusterJobs/Parser_AllRoots_nonLeaves/Parser_AllRoots_nonLeaves5_output.txt