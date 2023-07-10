#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/RandomFeatures/RandomFeatures$i.sh 
done
