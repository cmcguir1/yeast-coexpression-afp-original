#!/usr/bin/sh

## Job Created Oct-15-2024

##Place PBS directives here
#PBS -N OverfittingTest_3_200_50000
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 3 200 50000   > ClusterJobs/OverfittingTest/OverfittingTest7_output.txt