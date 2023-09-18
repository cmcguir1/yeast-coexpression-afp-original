#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/Dropout_OnlyPos/Dropout_OnlyPos$i.sh 
done
