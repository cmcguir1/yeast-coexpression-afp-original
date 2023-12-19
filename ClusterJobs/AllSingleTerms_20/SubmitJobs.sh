#!/usr/bin/sh

for i in {0..23}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms_20/AllSingleTerms_20$i.sh 
done
