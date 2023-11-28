#!/usr/bin/sh

for i in {0..107}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms/AllSingleTerms$i.sh 
done
