#!/usr/bin/sh

## Job Created Jul-10-2023

##Place PBS directives here
#PBS -N Overfit_Unreasonable
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3 250000    > ClusterJobs/Overfit_Unreasonable/Overfit_Unreasonable7_output.txt