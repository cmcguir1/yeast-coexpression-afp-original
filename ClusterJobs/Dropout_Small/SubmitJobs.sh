#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/Dropout_Small/Dropout_Small$i.sh 
done
