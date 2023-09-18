#!/usr/bin/sh

for i in {0..8}
do
	qsub data/SummerResearch2022/ClusterJobs/Opt_Dropout/Opt_Dropout$i.sh 
done
