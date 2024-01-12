#!/usr/bin/sh

## Job Created Jan-11-2024

##Place PBS directives here
#PBS -N CorrectedAnnos_Hetero_100_2
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main6.py 100 2    > ClusterJobs/CorrectedAnnos_Hetero/CorrectedAnnos_Hetero5_output.txt