#!/usr/bin/sh

## Job Created Jun-19-2023

##Place PBS directives here
#PBS -N MemMapTest
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 3 YeastDict_float16.npy    > ClusterJobs/MemMapTest/MemMapTest7_output.txt