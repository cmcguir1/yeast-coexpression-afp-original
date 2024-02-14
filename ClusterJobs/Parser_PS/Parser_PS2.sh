#!/usr/bin/sh

## Job Created Feb-14-2024

##Place PBS directives here
#PBS -N Parser_PS_0_200
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 0 200    > ClusterJobs/Parser_PS/Parser_PS2_output.txt