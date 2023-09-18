#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/WeightDecay/WeightDecay$i.sh 
done
