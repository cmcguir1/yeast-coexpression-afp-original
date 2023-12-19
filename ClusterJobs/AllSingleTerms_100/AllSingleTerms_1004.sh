#!/usr/bin/sh

## Job Created Dec-18-2023

##Place PBS directives here
#PBS -N AllSingleTerms_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms.py 4 100    > ClusterJobs/AllSingleTerms_100/AllSingleTerms_1004_output.txt