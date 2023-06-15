#!/usr/bin/sh

for i in {0..11}
do
	qsub data/SummerResearch2022/ClusterJobs/LossFunc/LossFunc$i.sh 
done
