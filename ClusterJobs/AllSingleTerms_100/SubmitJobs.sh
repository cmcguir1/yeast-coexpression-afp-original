#!/usr/bin/sh

for i in {0..9}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms_100/AllSingleTerms_100$i.sh 
done
