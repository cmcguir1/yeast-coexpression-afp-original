#!/usr/bin/sh

## Job Created Jan-25-2024

##Place PBS directives here
#PBS -N SmallestCommonAncestor
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main10.py      > ClusterJobs/SmallestCommonAncestor/SmallestCommonAncestor0_output.txt