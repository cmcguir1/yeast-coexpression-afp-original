#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/ZLPR_BCE_Comparison/ZLPR_BCE_Comparison$i.sh 
done
