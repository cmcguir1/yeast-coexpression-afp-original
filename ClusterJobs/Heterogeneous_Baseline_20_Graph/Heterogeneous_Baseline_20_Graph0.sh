#!/usr/bin/sh

## Job Created Nov-22-2023

##Place PBS directives here
#PBS -N Heterogeneous_Baseline_20_Graph
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py      > ClusterJobs/Heterogeneous_Baseline_20_Graph/Heterogeneous_Baseline_20_Graph0_output.txt