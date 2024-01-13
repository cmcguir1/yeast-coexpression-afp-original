#!/usr/bin/sh

## Job Created Jan-13-2024

##Place PBS directives here
#PBS -N Folds_bce_Original_Hetero_100_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 100 0    > ClusterJobs/Folds_bce_Original_Hetero/Folds_bce_Original_Hetero0_output.txt