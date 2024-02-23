#!/usr/bin/sh

## Job Created Feb-22-2024

##Place PBS directives here
#PBS -N Net_bcm_2_200x100
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 2 200x100    > ClusterJobs/Net_bcm/Net_bcm10_output.txt