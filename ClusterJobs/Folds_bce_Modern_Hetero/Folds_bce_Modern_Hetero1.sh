#!/usr/bin/sh

## Job Created Jan-11-2024

##Place PBS directives here
#PBS -N Folds_bce_Modern_Hetero_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 1     > ClusterJobs/Folds_bce_Modern_Hetero/Folds_bce_Modern_Hetero1_output.txt