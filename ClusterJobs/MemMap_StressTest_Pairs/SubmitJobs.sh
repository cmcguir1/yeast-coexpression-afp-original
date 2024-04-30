#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/MemMap_StressTest_Pairs/MemMap_StressTest_Pairs$i.sh 
done
