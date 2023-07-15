#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/Randomize_Control/Randomize_Control$i.sh 
done
