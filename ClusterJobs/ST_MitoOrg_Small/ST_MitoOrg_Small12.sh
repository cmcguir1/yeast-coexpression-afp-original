#!/usr/bin/sh

## Job Created Feb-26-2024

##Place PBS directives here
#PBS -N ST_MitoOrg_Small_0_10
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 0 10    > ClusterJobs/ST_MitoOrg_Small/ST_MitoOrg_Small12_output.txt