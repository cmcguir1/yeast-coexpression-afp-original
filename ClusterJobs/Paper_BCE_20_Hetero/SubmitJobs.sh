#!/usr/bin/sh

for i in {0..5}
do
	qsub data/SummerResearch2022/ClusterJobs/Paper_BCE_20_Hetero/Paper_BCE_20_Hetero$i.sh 
done
