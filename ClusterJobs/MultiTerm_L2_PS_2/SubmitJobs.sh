#!/usr/bin/sh

for i in {0..1}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_L2_PS_2/MultiTerm_L2_PS_2$i.sh 
done
