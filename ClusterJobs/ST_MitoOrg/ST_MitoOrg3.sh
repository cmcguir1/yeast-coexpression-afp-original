#!/usr/bin/sh

## Job Created Feb-24-2024

##Place PBS directives here
#PBS -N ST_MitoOrg_3_20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 3 20    > ClusterJobs/ST_MitoOrg/ST_MitoOrg3_output.txt