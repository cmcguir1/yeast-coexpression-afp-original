#!/usr/bin/sh

for i in {0..29}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms/AllSingleTerms$i.sh 
done
