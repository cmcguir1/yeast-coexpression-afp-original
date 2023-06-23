#!/usr/bin/sh

## Job Created Jun-23-2023

##Place PBS directives here
#PBS -N WCE
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 1 0.5    > ClusterJobs/WCE/WCE5_output.txt