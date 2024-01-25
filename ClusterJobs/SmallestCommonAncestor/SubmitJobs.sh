#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/SmallestCommonAncestor/SmallestCommonAncestor$i.sh 
done
