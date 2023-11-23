#!/usr/bin/sh

## Job Created Nov-22-2023

##Place PBS directives here
#PBS -N BCE_20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 3     > ClusterJobs/BCE_20/BCE_203_output.txt