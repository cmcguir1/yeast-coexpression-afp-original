#!/usr/bin/sh

## Job Created Jan-18-2024

##Place PBS directives here
#PBS -N Folds_bce_Modern_Hetero_100_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 100 0    > ClusterJobs/Folds_bce_Modern_Hetero/Folds_bce_Modern_Hetero0_output.txt