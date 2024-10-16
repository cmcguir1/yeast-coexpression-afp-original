#!/usr/bin/sh

## Job Created Oct-15-2024

##Place PBS directives here
#PBS -N OverfittingTest_1_500x200x100_300000
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 1 500x200x100 300000   > ClusterJobs/OverfittingTest/OverfittingTest17_output.txt