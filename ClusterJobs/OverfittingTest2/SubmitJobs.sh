#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/OverfittingTest2/OverfittingTest2$i.sh 
done
