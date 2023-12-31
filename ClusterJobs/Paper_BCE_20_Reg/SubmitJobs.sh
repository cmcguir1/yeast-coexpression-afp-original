#!/usr/bin/sh

for i in {0..1}
do
	qsub data/SummerResearch2022/ClusterJobs/Paper_BCE_20_Reg/Paper_BCE_20_Reg$i.sh 
done
