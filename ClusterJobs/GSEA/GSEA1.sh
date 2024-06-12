#!/usr/bin/sh

## Job Created Jun-11-2024

##Place PBS directives here
#PBS -N GSEA_SPELL
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/GSEA.py SPELL     > ClusterJobs/GSEA/GSEA1_output.txt