#!/usr/bin/sh

## Job Created Jan-01-2024

##Place PBS directives here
#PBS -N SingleTerm_PS_Reg_0.01_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main7.py 0.01 0    > ClusterJobs/SingleTerm_PS_Reg/SingleTerm_PS_Reg3_output.txt