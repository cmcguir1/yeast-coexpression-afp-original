#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/PosWeights_Control/PosWeights_Control$i.sh 
done
