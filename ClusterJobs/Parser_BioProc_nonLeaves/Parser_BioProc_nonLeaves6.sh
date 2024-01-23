#!/usr/bin/sh

## Job Created Jan-23-2024

##Place PBS directives here
#PBS -N Parser_BioProc_nonLeaves_2_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 2 1    > ClusterJobs/Parser_BioProc_nonLeaves/Parser_BioProc_nonLeaves6_output.txt