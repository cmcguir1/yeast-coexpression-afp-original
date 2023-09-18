#!/usr/bin/sh

## Job Created Sep-13-2023

##Place PBS directives here
#PBS -N Opt_WeightDecay
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 100 0.001    > ClusterJobs/Opt_WeightDecay/Opt_WeightDecay7_output.txt