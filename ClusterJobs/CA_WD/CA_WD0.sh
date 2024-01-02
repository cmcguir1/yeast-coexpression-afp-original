#!/usr/bin/sh

## Job Created Jan-02-2024

##Place PBS directives here
#PBS -N CA_WD_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 0     > ClusterJobs/CA_WD/CA_WD0_output.txt