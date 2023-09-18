#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/SmallStruct_WD/SmallStruct_WD$i.sh 
done
