#!/usr/bin/sh

<<<<<<< HEAD
## Job Created Jul-17-2023
=======
## Job Created Jul-15-2023
>>>>>>> 5ff3177fb48782f38673524226af2c09a7b921c5

##Place PBS directives here
#PBS -N Randomize_Control
#PBS -l nodes=1:ppn=36
#PBS -l walltime=168:00:00
#PBS -M cmcguir1@trinity.edu
#PBS -m ae

cd data/SummerResearch2022

<<<<<<< HEAD
/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3 200    > ClusterJobs/Randomize_Control/Randomize_Control3_output.txt
=======
/data/hibbslab/anaconda3/bin/python src/PairwiseYeastNetwork/Main4.py 3     > ClusterJobs/Randomize_Control/Randomize_Control3_output.txt
>>>>>>> 5ff3177fb48782f38673524226af2c09a7b921c5
