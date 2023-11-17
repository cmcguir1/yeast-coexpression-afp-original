#!/usr/bin/sh

## Job Created Nov-17-2023

##Place PBS directives here
#PBS -N Heterogeneous_Reg_20_Graph
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3     > ClusterJobs/Heterogeneous_Reg_20_Graph/Heterogeneous_Reg_20_Graph3_output.txt