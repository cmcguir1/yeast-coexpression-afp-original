#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/CorrelationRecalc/CorrelationRecalc$i.sh 
done
