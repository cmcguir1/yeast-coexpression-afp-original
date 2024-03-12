#!/usr/bin/sh

## Job Created Mar-11-2024

##Place PBS directives here
#PBS -N ST_MitoOrg_L2_PS_0.5_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py 0.5 100    > ClusterJobs/ST_MitoOrg_L2_PS/ST_MitoOrg_L2_PS1_output.txt