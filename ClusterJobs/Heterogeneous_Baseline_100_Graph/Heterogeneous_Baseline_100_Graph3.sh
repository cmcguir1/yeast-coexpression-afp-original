#!/usr/bin/sh

## Job Created Nov-21-2023

##Place PBS directives here
#PBS -N Heterogeneous_Baseline_100_Graph
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 3     > ClusterJobs/Heterogeneous_Baseline_100_Graph/Heterogeneous_Baseline_100_Graph3_output.txt