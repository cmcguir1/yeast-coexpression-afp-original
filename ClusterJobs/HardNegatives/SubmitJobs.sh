#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/HardNegatives/HardNegatives$i.sh 
done
