#!/usr/bin/sh

for i in {0..3}
do
	qsub data/SummerResearch2022/ClusterJobs/SingleTerm_2.28/SingleTerm_2.28$i.sh 
done
