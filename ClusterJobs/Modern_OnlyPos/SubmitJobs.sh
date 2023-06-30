#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Modern_OnlyPos/Modern_OnlyPos$i.sh 
done
