#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_NetStruct_PS_Modern/MultiTerm_NetStruct_PS_Modern$i.sh 
done
