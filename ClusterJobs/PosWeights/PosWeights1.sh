#!/usr/bin/sh

## Job Created Feb-15-2024

##Place PBS directives here
#PBS -N PosWeights_0_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 0 1    > ClusterJobs/PosWeights/PosWeights1_output.txt