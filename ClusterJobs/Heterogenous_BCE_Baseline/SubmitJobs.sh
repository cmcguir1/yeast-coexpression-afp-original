#!/usr/bin/sh

for i in {0..1}
do
	qsub data/SummerResearch2022/ClusterJobs/Heterogenous_BCE_Baseline/Heterogenous_BCE_Baseline$i.sh 
done
