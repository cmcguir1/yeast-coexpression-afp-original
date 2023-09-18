#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/Deep_SmallStruct/Deep_SmallStruct$i.sh 
done
