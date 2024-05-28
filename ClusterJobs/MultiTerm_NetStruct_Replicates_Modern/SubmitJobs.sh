#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_NetStruct_Replicates_Modern/MultiTerm_NetStruct_Replicates_Modern$i.sh 
done
