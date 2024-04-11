#!/usr/bin/sh

## Job Created Apr-11-2024

##Place PBS directives here
#PBS -N ST_PS_Term_MitoOrg_GO:0006486_0.01
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py GO:0006486 0.01    > ClusterJobs/ST_PS_Term_MitoOrg/ST_PS_Term_MitoOrg7_output.txt