#!/usr/bin/sh

## Job Created Jan-01-2024

##Place PBS directives here
#PBS -N MitoInheritance_Graph_2_20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/MitoInheritance.py 2 20    > ClusterJobs/MitoInheritance_Graph/MitoInheritance_Graph2_output.txt