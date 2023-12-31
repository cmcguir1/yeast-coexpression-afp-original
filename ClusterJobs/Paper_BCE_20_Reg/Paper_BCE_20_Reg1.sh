#!/usr/bin/sh

## Job Created Dec-31-2023

##Place PBS directives here
#PBS -N Paper_BCE_20_Reg_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 100     > ClusterJobs/Paper_BCE_20_Reg/Paper_BCE_20_Reg1_output.txt