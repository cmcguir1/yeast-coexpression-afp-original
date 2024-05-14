#!/usr/bin/sh

for i in {0..15}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_LinearEval_Replicate/MultiTerm_LinearEval_Replicate$i.sh 
done
