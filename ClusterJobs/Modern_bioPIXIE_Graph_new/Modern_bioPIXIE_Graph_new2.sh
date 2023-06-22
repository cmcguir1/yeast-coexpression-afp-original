#!/usr/bin/sh

## Job Created Jun-21-2023

##Place PBS directives here
#PBS -N Modern_bioPIXIE_Graph_new
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main6.py 2     > ClusterJobs/Modern_bioPIXIE_Graph_new/Modern_bioPIXIE_Graph_new2_output.txt