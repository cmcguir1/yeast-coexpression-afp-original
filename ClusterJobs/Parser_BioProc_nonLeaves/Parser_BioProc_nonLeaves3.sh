#!/usr/bin/sh

## Job Created Jan-22-2024

##Place PBS directives here
#PBS -N Parser_BioProc_nonLeaves_3
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 3     > ClusterJobs/Parser_BioProc_nonLeaves/Parser_BioProc_nonLeaves3_output.txt