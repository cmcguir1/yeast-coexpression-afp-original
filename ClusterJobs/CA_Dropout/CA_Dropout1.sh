#!/usr/bin/sh

## Job Created Jan-02-2024

##Place PBS directives here
#PBS -N CA_Dropout_1_0.1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 1 0.1    > ClusterJobs/CA_Dropout/CA_Dropout1_output.txt