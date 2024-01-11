#!/usr/bin/sh

## Job Created Jan-10-2024

##Place PBS directives here
#PBS -N CorrectedAnnos_100_3
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main.py 100 3    > ClusterJobs/CorrectedAnnos/CorrectedAnnos7_output.txt