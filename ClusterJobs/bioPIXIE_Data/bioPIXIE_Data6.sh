#!/usr/bin/sh

## Job Created May-26-2023

##Place PBS directives here
#PBS -N bioPIXIE_Data
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 2 25000   