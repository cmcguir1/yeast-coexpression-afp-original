#!/usr/bin/sh

for i in {0..53}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms_20_CT/AllSingleTerms_20_CT$i.sh 
done
