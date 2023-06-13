#!/usr/bin/sh

## Job Created Jun-12-2023

##Place PBS directives here
#PBS -N ST_ParaSearch
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/SingleTermMain.py GO:0007005 500 0.1 runAll 