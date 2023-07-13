#!/usr/bin/sh

## Job Created Jul-13-2023

##Place PBS directives here
#PBS -N Random_SwapGenesTest
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 0     > ClusterJobs/Random_SwapGenesTest/Random_SwapGenesTest0_output.txt