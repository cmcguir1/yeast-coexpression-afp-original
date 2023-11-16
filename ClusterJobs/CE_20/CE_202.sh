#!/usr/bin/sh

## Job Created Nov-16-2023

##Place PBS directives here
#PBS -N CE_20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main11.py 2     > ClusterJobs/CE_20/CE_202_output.txt