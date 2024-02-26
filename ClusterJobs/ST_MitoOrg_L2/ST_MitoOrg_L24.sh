#!/usr/bin/sh

## Job Created Feb-26-2024

##Place PBS directives here
#PBS -N ST_MitoOrg_L2_0_0.001
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0 0.001    > ClusterJobs/ST_MitoOrg_L2/ST_MitoOrg_L24_output.txt