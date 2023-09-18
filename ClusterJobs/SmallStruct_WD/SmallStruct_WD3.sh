#!/usr/bin/sh

## Job Created Jul-19-2023

##Place PBS directives here
#PBS -N SmallStruct_WD
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 20 0.01    > ClusterJobs/SmallStruct_WD/SmallStruct_WD3_output.txt