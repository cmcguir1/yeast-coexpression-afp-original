#!/usr/bin/sh

## Job Created Sep-25-2023

##Place PBS directives here
#PBS -N LossFunc_Redo_BCE
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 2 20    > ClusterJobs/LossFunc_Redo_BCE/LossFunc_Redo_BCE2_output.txt