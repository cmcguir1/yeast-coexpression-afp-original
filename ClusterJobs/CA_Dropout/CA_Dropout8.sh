#!/usr/bin/sh

## Job Created Jan-02-2024

##Place PBS directives here
#PBS -N CA_Dropout_0_0.001
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 0 0.001    > ClusterJobs/CA_Dropout/CA_Dropout8_output.txt