#!/usr/bin/sh

## Job Created Nov-21-2023

##Place PBS directives here
#PBS -N Heterogenous_BCE_Reg_20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main12.py 2     > ClusterJobs/Heterogenous_BCE_Reg_20/Heterogenous_BCE_Reg_202_output.txt