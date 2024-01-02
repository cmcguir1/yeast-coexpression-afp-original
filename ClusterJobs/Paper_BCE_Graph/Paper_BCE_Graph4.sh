#!/usr/bin/sh

## Job Created Jan-01-2024

##Place PBS directives here
#PBS -N Paper_BCE_Graph_20_2
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 20 2    > ClusterJobs/Paper_BCE_Graph/Paper_BCE_Graph4_output.txt