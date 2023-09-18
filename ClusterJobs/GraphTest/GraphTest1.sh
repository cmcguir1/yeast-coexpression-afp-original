#!/usr/bin/sh

## Job Created Jul-19-2023

##Place PBS directives here
#PBS -N GraphTest
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/GraphMain.py 1     > ClusterJobs/GraphTest/GraphTest1_output.txt