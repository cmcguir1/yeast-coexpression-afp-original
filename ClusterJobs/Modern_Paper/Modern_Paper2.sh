#!/usr/bin/sh

## Job Created Jan-02-2024

##Place PBS directives here
#PBS -N Modern_Paper_200
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 200     > ClusterJobs/Modern_Paper/Modern_Paper2_output.txt