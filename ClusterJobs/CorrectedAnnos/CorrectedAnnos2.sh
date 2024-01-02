#!/usr/bin/sh

## Job Created Jan-02-2024

##Place PBS directives here
#PBS -N CorrectedAnnos_20_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 20 1    > ClusterJobs/CorrectedAnnos/CorrectedAnnos2_output.txt