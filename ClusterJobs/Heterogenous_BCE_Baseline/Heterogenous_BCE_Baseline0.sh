#!/usr/bin/sh

## Job Created Oct-29-2023

##Place PBS directives here
#PBS -N Heterogenous_BCE_Baseline
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main9.py 20     > ClusterJobs/Heterogenous_BCE_Baseline/Heterogenous_BCE_Baseline0_output.txt