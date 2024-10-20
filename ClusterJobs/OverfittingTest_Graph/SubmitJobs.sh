#!/usr/bin/sh

for i in {0..31}
do
	qsub data/SummerResearch2022/ClusterJobs/OverfittingTest_Graph/OverfittingTest_Graph$i.sh 
done
