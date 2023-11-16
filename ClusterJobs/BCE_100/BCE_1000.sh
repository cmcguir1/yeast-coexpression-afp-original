#!/usr/bin/sh

## Job Created Nov-16-2023

##Place PBS directives here
#PBS -N BCE_100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main9.py 0     > ClusterJobs/BCE_100/BCE_1000_output.txt