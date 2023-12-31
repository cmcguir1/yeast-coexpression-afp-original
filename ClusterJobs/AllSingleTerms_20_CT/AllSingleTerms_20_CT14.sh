#!/usr/bin/sh

## Job Created Dec-31-2023

##Place PBS directives here
#PBS -N AllSingleTerms_20_CT_14_20
#PBS -l nodes=n19:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms.py 14 20    > ClusterJobs/AllSingleTerms_20_CT/AllSingleTerms_20_CT14_output.txt