#!/usr/bin/sh

## Job Created Dec-28-2023

##Place PBS directives here
#PBS -N AllSingleTerms_20_12.23.2023_47_20
#PBS -l nodes=n18:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms.py 47 20    > ClusterJobs/AllSingleTerms_20_12.23.2023/AllSingleTerms_20_12.23.202347_output.txt