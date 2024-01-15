#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/Folds_bce_Modern_Hetero/Folds_bce_Modern_Hetero$i.sh 
done
