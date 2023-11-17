#!/usr/bin/sh

## Job Created Nov-17-2023

##Place PBS directives here
#PBS -N CE_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main10.py      > ClusterJobs/CE_100/CE_1000_output.txt