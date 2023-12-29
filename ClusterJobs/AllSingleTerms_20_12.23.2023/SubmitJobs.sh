#!/usr/bin/sh

for i in {0..53}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms_20_12.23.2023/AllSingleTerms_20_12.23.2023$i.sh 
done
