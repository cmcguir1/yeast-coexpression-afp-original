#!/usr/bin/sh

for i in {0..4}
do
	qsub data/SummerResearch2022/ClusterJobs/ConsistencyReplicates_DiffFold/ConsistencyReplicates_DiffFold$i.sh 
done
