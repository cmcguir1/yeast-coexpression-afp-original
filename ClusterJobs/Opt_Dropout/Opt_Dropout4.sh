#!/usr/bin/sh

## Job Created Sep-13-2023

##Place PBS directives here
#PBS -N Opt_Dropout
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 100 0.3    > ClusterJobs/Opt_Dropout/Opt_Dropout4_output.txt