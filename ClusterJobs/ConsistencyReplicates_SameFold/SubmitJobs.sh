#!/usr/bin/sh

for i in {0..4}
do
	qsub data/SummerResearch2022/ClusterJobs/ConsistencyReplicates_SameFold/ConsistencyReplicates_SameFold$i.sh 
done
