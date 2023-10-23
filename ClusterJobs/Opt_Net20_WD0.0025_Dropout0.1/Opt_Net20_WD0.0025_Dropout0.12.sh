#!/usr/bin/sh

## Job Created Oct-23-2023

##Place PBS directives here
#PBS -N Opt_Net20_WD0.0025_Dropout0.1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 2     > ClusterJobs/Opt_Net20_WD0.0025_Dropout0.1/Opt_Net20_WD0.0025_Dropout0.12_output.txt