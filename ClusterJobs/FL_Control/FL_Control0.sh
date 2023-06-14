#!/usr/bin/sh

## Job Created Jun-14-2023

##Place PBS directives here
#PBS -N FL_Control
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main6.py 0 FL    > ClusterJobs/FL_Control/FL_Control0_output.txt