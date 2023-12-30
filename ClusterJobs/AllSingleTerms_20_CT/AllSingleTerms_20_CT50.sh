#!/usr/bin/sh

## Job Created Dec-29-2023

##Place PBS directives here
#PBS -N AllSingleTerms_20_CT_50_20
#PBS -l nodes=n21:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms.py 50 20    > ClusterJobs/AllSingleTerms_20_CT/AllSingleTerms_20_CT50_output.txt