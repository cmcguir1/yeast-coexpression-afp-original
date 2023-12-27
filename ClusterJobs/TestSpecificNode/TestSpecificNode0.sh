#!/usr/bin/sh

## Job Created Dec-27-2023

##Place PBS directives here
#PBS -N TestSpecificNode
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -l node=n3
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/TestArea.py      > ClusterJobs/TestSpecificNode/TestSpecificNode0_output.txt