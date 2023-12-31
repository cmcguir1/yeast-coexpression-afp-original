#!/usr/bin/sh

## Job Created Dec-31-2023

##Place PBS directives here
#PBS -N BCE_20_Sigmoid_True
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/GraphMain.py True     > ClusterJobs/BCE_20_Sigmoid/BCE_20_Sigmoid0_output.txt