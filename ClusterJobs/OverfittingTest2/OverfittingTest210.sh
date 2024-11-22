#!/usr/bin/sh

## Job Created Nov-22-2024

##Place PBS directives here
#PBS -N OverfittingTest2_2_20x20x20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 2 20x20x20    > ClusterJobs/OverfittingTest2/OverfittingTest210_output.txt