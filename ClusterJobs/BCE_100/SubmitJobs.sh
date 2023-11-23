#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/BCE_100/BCE_100$i.sh 
done
