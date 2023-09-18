#!/usr/bin/sh

## Job Created Jul-19-2023

##Place PBS directives here
#PBS -N SmallStruct
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 0 20    > ClusterJobs/SmallStruct/SmallStruct8_output.txt