#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/MemMap_Debug/MemMap_Debug$i.sh 
done
