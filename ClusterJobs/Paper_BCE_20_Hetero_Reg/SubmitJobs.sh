#!/usr/bin/sh

for i in {0..5}
do
	qsub data/SummerResearch2022/ClusterJobs/Paper_BCE_20_Hetero_Reg/Paper_BCE_20_Hetero_Reg$i.sh 
done
