#!/usr/bin/sh

## Job Created Jun-29-2023

##Place PBS directives here
#PBS -N Modern_OnlyPos
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 0     > ClusterJobs/Modern_OnlyPos/Modern_OnlyPos0_output.txt