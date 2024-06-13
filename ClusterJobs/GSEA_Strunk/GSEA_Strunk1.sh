#!/usr/bin/sh

## Job Created Jun-13-2024

##Place PBS directives here
#PBS -N GSEA_Strunk_1
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/GSEA_strunk.py 1     > ClusterJobs/GSEA_Strunk/GSEA_Strunk1_output.txt