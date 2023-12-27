#!/usr/bin/sh

## Job Created Dec-27-2023

##Place PBS directives here
#PBS -N MitoInheritance
#PBS -l nodes=n6:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/MitoInheritance.py 2 20    > ClusterJobs/MitoInheritance/MitoInheritance2_output.txt