#!/usr/bin/sh

## Job Created Jan-30-2024

##Place PBS directives here
#PBS -N Parser_AllRoots_nonLeaves_2
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 2     > ClusterJobs/Parser_AllRoots_nonLeaves/Parser_AllRoots_nonLeaves2_output.txt