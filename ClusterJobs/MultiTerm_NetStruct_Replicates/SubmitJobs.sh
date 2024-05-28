#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_NetStruct_Replicates/MultiTerm_NetStruct_Replicates$i.sh 
done
