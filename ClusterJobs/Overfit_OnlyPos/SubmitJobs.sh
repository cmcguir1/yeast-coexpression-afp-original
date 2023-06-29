#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/Overfit_OnlyPos/Overfit_OnlyPos$i.sh 
done
