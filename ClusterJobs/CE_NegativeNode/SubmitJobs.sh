#!/usr/bin/sh

for i in {0..2}
do
	qsub data/SummerResearch2022/ClusterJobs/CE_NegativeNode/CE_NegativeNode$i.sh 
done
