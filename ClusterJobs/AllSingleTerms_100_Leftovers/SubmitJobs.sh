#!/usr/bin/sh

for i in {0..14}
do
	qsub data/SummerResearch2022/ClusterJobs/AllSingleTerms_100_Leftovers/AllSingleTerms_100_Leftovers$i.sh 
done
