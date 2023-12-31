#!/usr/bin/sh

## Job Created Dec-31-2023

##Place PBS directives here
#PBS -N MitoInheritance_2_20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/MitoInheritance.py 2 20    > ClusterJobs/MitoInheritance/MitoInheritance2_output.txt