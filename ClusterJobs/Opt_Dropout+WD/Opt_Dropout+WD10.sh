#!/usr/bin/sh

## Job Created Sep-28-2023

##Place PBS directives here
#PBS -N Opt_Dropout+WD
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 20 0.5 0.0025   > ClusterJobs/Opt_Dropout+WD/Opt_Dropout+WD10_output.txt