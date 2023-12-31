#!/usr/bin/sh

## Job Created Dec-31-2023

##Place PBS directives here
#PBS -N Paper_BCE_20_Hetero_200_0.1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 200 0.1    > ClusterJobs/Paper_BCE_20_Hetero/Paper_BCE_20_Hetero2_output.txt