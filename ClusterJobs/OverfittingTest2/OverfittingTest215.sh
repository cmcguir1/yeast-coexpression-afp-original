#!/usr/bin/sh

## Job Created Oct-17-2024

##Place PBS directives here
#PBS -N OverfittingTest2_3_20x20x20_300000
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3 20x20x20 300000   > ClusterJobs/OverfittingTest2/OverfittingTest215_output.txt