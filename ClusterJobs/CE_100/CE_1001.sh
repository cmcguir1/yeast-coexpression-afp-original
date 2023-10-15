#!/usr/bin/sh

## Job Created Oct-15-2023

##Place PBS directives here
#PBS -N CE_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main6.py 1     > ClusterJobs/CE_100/CE_1001_output.txt