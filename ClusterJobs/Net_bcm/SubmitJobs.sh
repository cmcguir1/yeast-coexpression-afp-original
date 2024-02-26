#!/usr/bin/sh

for i in {0..19}
do
	qsub data/SummerResearch2022/ClusterJobs/Net_bcm/Net_bcm$i.sh 
done
