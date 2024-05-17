#!/usr/bin/sh

for i in {0..7}
do
	qsub data/SummerResearch2022/ClusterJobs/MultiTerm_LinearEval_Replicate_Parallel/MultiTerm_LinearEval_Replicate_Parallel$i.sh 
done
