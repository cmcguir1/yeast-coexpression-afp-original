#!/usr/bin/sh

## Job Created Mar-23-2024

##Place PBS directives here
#PBS -N ST_PS_Term_GO:0006260_0.2
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py GO:0006260 0.2    > ClusterJobs/ST_PS_Term/ST_PS_Term7_output.txt