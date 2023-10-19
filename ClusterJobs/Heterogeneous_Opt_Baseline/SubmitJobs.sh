#!/usr/bin/sh

for i in {0..1}
do
	qsub data/SummerResearch2022/ClusterJobs/Heterogeneous_Opt_Baseline/Heterogeneous_Opt_Baseline$i.sh 
done
