#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/FocalLoss_Control/FocalLoss_Control$i.sh 
done
