#!/usr/bin/sh

for i in {0..23}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_L2_PS/MultiTerm_L2_PS$i.sh 
done
