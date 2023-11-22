#!/usr/bin/sh

## Job Created Nov-22-2023

##Place PBS directives here
#PBS -N Heterogeneous_Reg_100_Graph
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 3     > ClusterJobs/Heterogeneous_Reg_100_Graph/Heterogeneous_Reg_100_Graph3_output.txt