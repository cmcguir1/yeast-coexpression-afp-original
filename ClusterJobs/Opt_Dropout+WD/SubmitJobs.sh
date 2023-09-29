#!/usr/bin/sh

for i in {0..23}
do
	qsub data/SummerResearch2022/ClusterJobs/Opt_Dropout+WD/Opt_Dropout+WD$i.sh 
done
