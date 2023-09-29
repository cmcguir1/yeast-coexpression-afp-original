#!/usr/bin/sh

<<<<<<< HEAD
## Job Created Jul-17-2023
=======
## Job Created Jul-15-2023
>>>>>>> 5ff3177fb48782f38673524226af2c09a7b921c5

##Place PBS directives here
#PBS -N Random_SwapGenes
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

<<<<<<< HEAD
/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 0 200    > ClusterJobs/Random_SwapGenes/Random_SwapGenes0_output.txt
=======
/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main2.py 0     > ClusterJobs/Random_SwapGenes/Random_SwapGenes0_output.txt
>>>>>>> 5ff3177fb48782f38673524226af2c09a7b921c5
