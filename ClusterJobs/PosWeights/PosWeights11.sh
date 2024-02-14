#!/usr/bin/sh

## Job Created Feb-14-2024

##Place PBS directives here
#PBS -N PosWeights_3_10
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3 10    > ClusterJobs/PosWeights/PosWeights11_output.txt