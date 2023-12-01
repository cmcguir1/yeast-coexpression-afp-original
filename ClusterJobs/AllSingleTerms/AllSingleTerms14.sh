#!/usr/bin/sh

## Job Created Nov-30-2023

##Place PBS directives here
#PBS -N AllSingleTerms
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/AllSingleTerms.py 14 20    > ClusterJobs/AllSingleTerms/AllSingleTerms14_output.txt