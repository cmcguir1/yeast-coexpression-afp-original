#!/usr/bin/sh

## Job Created Jun-28-2023

##Place PBS directives here
#PBS -N RandomizedLabels
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0     > ClusterJobs/RandomizedLabels/RandomizedLabels0_output.txt