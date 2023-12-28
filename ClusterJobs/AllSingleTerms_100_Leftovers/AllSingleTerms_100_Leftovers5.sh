#!/usr/bin/sh

## Job Created Dec-28-2023

##Place PBS directives here
#PBS -N AllSingleTerms_100_Leftovers_5_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms_Leftovers.py 5 100    > ClusterJobs/AllSingleTerms_100_Leftovers/AllSingleTerms_100_Leftovers5_output.txt