#!/usr/bin/sh

## Job Created Jul-18-2023

##Place PBS directives here
#PBS -N Batch_SmallStruct
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 1 1    > ClusterJobs/Batch_SmallStruct/Batch_SmallStruct1_output.txt