#!/usr/bin/sh

## Job Created Jan-25-2024

##Place PBS directives here
#PBS -N Batch_PS_5000_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 5000 1    > ClusterJobs/Batch_PS/Batch_PS2_output.txt