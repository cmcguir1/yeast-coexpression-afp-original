#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/lr_OnlyPos/lr_OnlyPos$i.sh 
done
