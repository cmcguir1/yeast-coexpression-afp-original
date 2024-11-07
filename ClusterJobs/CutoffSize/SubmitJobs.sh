#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/CutoffSize/CutoffSize$i.sh 
done
