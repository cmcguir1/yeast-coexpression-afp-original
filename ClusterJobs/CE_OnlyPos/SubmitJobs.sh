#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/CE_OnlyPos/CE_OnlyPos$i.sh 
done
