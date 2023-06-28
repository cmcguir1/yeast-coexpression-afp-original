#!/usr/bin/sh

for i in {0..23}
do
	qsub data/SummerResearch2022/ClusterJobs/OnlyPos_ps/OnlyPos_ps$i.sh 
done
