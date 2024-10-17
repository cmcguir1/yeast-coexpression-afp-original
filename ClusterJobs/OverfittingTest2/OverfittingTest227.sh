#!/usr/bin/sh

## Job Created Oct-17-2024

##Place PBS directives here
#PBS -N OverfittingTest2_3_80x80x80_600000
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3 80x80x80 600000   > ClusterJobs/OverfittingTest2/OverfittingTest227_output.txt