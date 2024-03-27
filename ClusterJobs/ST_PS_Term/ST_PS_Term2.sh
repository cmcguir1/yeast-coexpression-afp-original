#!/usr/bin/sh

## Job Created Mar-27-2024

##Place PBS directives here
#PBS -N ST_PS_Term_GO:0006486_0.1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py GO:0006486 0.1    > ClusterJobs/ST_PS_Term/ST_PS_Term2_output.txt