#!/usr/bin/sh

for i in {0..31}
do
	qsub data/SummerResearch2022/ClusterJobs/OverfittingTest/OverfittingTest$i.sh 
done
