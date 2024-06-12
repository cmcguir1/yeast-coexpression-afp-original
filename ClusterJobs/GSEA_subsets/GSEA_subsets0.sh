#!/usr/bin/sh

## Job Created Jun-12-2024

##Place PBS directives here
#PBS -N GSEA_subsets_NN
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/GSEA.py NN     > ClusterJobs/GSEA_subsets/GSEA_subsets0_output.txt