#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Heterogeneous_Baseline_100_Graph/Heterogeneous_Baseline_100_Graph$i.sh 
done
