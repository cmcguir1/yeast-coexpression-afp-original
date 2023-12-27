#!/usr/bin/sh

## Job Created Dec-27-2023

##Place PBS directives here
#PBS -N AllSingleTerms_100_Leftovers
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms_Leftovers.py 10 100    > ClusterJobs/AllSingleTerms_100_Leftovers/AllSingleTerms_100_Leftovers10_output.txt