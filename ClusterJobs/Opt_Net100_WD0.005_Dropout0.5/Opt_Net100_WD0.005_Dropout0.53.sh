#!/usr/bin/sh

## Job Created Nov-22-2023

##Place PBS directives here
#PBS -N Opt_Net100_WD0.005_Dropout0.5
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main6.py 3     > ClusterJobs/Opt_Net100_WD0.005_Dropout0.5/Opt_Net100_WD0.005_Dropout0.53_output.txt