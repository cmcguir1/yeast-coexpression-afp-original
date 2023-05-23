#!/usr/bin/sh

## Job Created May-23-2023

##Place PBS directives here
#PBS -N BioProc+Local_Graph
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

touch data/SummerResearch2022/ClusterJobs/BioProc+Local_Graph/BioProc+Local_Graph7_output.txt
/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/GraphMain.py 3 2000    &> data/SummerResearch2022/ClusterJobs/BioProc+Local_Graph/BioProc+Local_Graph7_output.txt