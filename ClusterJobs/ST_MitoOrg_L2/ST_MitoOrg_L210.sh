#!/usr/bin/sh

## Job Created Feb-26-2024

##Place PBS directives here
#PBS -N ST_MitoOrg_L2_2_1e-05
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 2 1e-05    > ClusterJobs/ST_MitoOrg_L2/ST_MitoOrg_L210_output.txt