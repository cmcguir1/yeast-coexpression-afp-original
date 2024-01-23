#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/Parser_AllRoots_nonLeaves/Parser_AllRoots_nonLeaves$i.sh 
done
