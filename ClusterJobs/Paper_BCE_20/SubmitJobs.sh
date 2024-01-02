#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/Paper_BCE_20/Paper_BCE_20$i.sh 
done
