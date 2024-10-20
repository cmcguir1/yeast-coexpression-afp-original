#!/usr/bin/sh

## Job Created Oct-20-2024

##Place PBS directives here
#PBS -N OverfittingTest2_2_80_600000
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 2 80 600000   > ClusterJobs/OverfittingTest2/OverfittingTest222_output.txt