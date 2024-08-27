#!/usr/bin/sh

## Job Created Jul-23-2024

##Place PBS directives here
#PBS -N ZLPR_BCE_Comparison_2_BCE
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 2 BCE    > ClusterJobs/ZLPR_BCE_Comparison/ZLPR_BCE_Comparison6_output.txt