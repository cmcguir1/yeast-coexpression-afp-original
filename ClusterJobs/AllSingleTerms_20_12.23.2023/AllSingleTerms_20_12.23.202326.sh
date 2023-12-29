#!/usr/bin/sh

## Job Created Dec-28-2023

##Place PBS directives here
#PBS -N AllSingleTerms_20_12.23.2023_26_20
#PBS -l nodes=n31:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms.py 26 20    > ClusterJobs/AllSingleTerms_20_12.23.2023/AllSingleTerms_20_12.23.202326_output.txt