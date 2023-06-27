#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/UnrelatedNode/UnrelatedNode$i.sh 
done
