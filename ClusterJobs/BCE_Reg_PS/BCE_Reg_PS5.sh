#!/usr/bin/sh

## Job Created Jan-01-2024

##Place PBS directives here
#PBS -N BCE_Reg_PS_0.0001_0.1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0.0001 0.1    > ClusterJobs/BCE_Reg_PS/BCE_Reg_PS5_output.txt