#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/LossFunc2/LossFunc2$i.sh 
done
