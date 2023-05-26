#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/FocalLoss_ParaSearch/FocalLoss_ParaSearch$i.sh 
done
