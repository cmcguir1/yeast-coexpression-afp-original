#!/usr/bin/sh

## Job Created Apr-11-2024

##Place PBS directives here
#PBS -N ST_PS_Term_MitoOrg_GO:0007005_0.1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py GO:0007005 0.1    > ClusterJobs/ST_PS_Term_MitoOrg/ST_PS_Term_MitoOrg3_output.txt