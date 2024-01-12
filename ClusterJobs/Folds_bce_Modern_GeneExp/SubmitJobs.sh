#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Folds_bce_Modern_GeneExp/Folds_bce_Modern_GeneExp$i.sh 
done
