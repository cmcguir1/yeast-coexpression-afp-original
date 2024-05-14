#!/usr/bin/sh

for i in {0..0}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_LinearEval/MultiTerm_LinearEval$i.sh 
done
