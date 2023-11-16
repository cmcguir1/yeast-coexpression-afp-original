#!/usr/bin/sh

## Job Created Nov-16-2023

##Place PBS directives here
#PBS -N Heterogenous_BCE_Baseline
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main9.py 100     > ClusterJobs/Heterogenous_BCE_Baseline/Heterogenous_BCE_Baseline1_output.txt