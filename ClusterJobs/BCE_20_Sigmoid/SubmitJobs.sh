#!/usr/bin/sh

for i in {0..1}
do
	qsub data/SummerResearch2022/ClusterJobs/BCE_20_Sigmoid/BCE_20_Sigmoid$i.sh 
done
