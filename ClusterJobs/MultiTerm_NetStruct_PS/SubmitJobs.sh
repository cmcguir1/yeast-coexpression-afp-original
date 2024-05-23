#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_NetStruct_PS/MultiTerm_NetStruct_PS$i.sh 
done
