#!/usr/bin/sh

## Job Created Jan-23-2024

##Place PBS directives here
#PBS -N Batch_PS_50_4
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 50 4    > ClusterJobs/Batch_PS/Batch_PS9_output.txt