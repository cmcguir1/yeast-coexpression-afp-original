#!/usr/bin/sh

## Job Created Jan-04-2024

##Place PBS directives here
#PBS -N CorrectedAnnos_Hetero_20_0
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main3.py 20 0    > ClusterJobs/CorrectedAnnos_Hetero/CorrectedAnnos_Hetero0_output.txt