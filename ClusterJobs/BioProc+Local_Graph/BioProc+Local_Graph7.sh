#!/usr/bin/sh

## Job Created May-25-2023

##Place PBS directives here
#PBS -N BioProc+Local_Graph
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/GraphMain.py 3 2000   