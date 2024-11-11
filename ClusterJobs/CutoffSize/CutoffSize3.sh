#!/usr/bin/sh

## Job Created Nov-10-2024

##Place PBS directives here
#PBS -N CutoffSize_3_19_20x20x20
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main8.py 3 19 20x20x20   > ClusterJobs/CutoffSize/CutoffSize3_output.txt