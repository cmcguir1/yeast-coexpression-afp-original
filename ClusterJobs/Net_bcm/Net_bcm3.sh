#!/usr/bin/sh

## Job Created Feb-26-2024

##Place PBS directives here
#PBS -N Net_bcm_0_500
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 0 500    > ClusterJobs/Net_bcm/Net_bcm3_output.txt