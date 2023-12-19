#!/usr/bin/sh

for i in {0..9}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms/AllSingleTerms$i.sh 
done
