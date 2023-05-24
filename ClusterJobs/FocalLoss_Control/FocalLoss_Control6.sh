#!/usr/bin/sh

## Job Created May-24-2023

##Place PBS directives here
#PBS -N FocalLoss_Control
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/TestMain.py 2 CE   