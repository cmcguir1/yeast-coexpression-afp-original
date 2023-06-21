#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/LR_ps/LR_ps$i.sh 
done
