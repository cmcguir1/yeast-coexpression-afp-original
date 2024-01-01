#!/usr/bin/sh

## Job Created Jan-01-2024

##Place PBS directives here
#PBS -N BCE_Reg_PS_0_0.5
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main5.py 0 0.5    > ClusterJobs/BCE_Reg_PS/BCE_Reg_PS8_output.txt