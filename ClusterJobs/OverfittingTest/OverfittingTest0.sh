#!/usr/bin/sh

## Job Created Oct-15-2024

##Place PBS directives here
#PBS -N OverfittingTest_0_500x200x100_50000
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 0 500x200x100 50000   > ClusterJobs/OverfittingTest/OverfittingTest0_output.txt