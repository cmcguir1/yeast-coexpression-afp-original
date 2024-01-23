#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/Parser_AllRoots/Parser_AllRoots$i.sh 
done
